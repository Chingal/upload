import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from apps.tickets.models import Ticket, File
from apps.tickets.tasks import Upload

from .serializers import TicketSerializer, FileSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import TicketLimitOffsetPagination, TicketPageNumberPagination


class TicketList(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    name = 'ticket-list'
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = TicketPageNumberPagination
    #filter_backends = (filters.DjangoFilterBackend,)
    #filter_class = TicketFilter

    def get_queryset(self):
        user = self.request.user  # Current User
        status = self.request.GET.get('status')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')        
        kwargs = {}
        if status:
            kwargs['status__icontains'] = status
        if start_date and end_date:
            kwargs['created_at__range'] = (start_date, end_date)
        if start_date:
            kwargs['created_at__gte'] = start_date
        if end_date:
            kwargs['created_at__lte'] = end_date

        return Ticket.objects.filter(user=user, **kwargs)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketDetail(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    name = 'ticket-detail'
    lookup_field = 'pk'
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    

class FileList(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    name = 'file-list'
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        file = self.request.FILES.get('file', False)
        if file:
            temp_file = default_storage.save('tmp/' + str(file), ContentFile(file.read()))
            tmp_file_path = os.path.join(settings.MEDIA_ROOT, temp_file)
            Upload.delay(tmp_file_path, self.request.data['ticket'])


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return Response({
            'tickets': reverse(TicketList.name, request=request),
            'files': reverse(FileList.name, request=request),
        })