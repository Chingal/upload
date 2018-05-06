from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from apps.tickets.models import Ticket, File
from .serializers import TicketSerializer, FileSerializer
from .tasks import Upload
from .filters import TicketFilter


class TicketList(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    name = 'ticket-list'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TicketFilter

    def get_queryset(self):
        user = self.request.user  # Current User
        return Ticket.objects.filter(user=user).order_by('id')  # Filter drones by current user and ordered by id

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketDetail(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    name = 'ticket-detail'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class FileList(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    name = 'file-list'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(id=self.request.data['ticket'])
        files = self.get_queryset().filter(ticket=ticket)
        if files.count() < ticket.limit:
            Upload.delay(self.request.FILES['file'], self.request.user)
        serializer.save(file=self.request.data.get('file'))


class FileDetail(generics.RetrieveAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    name = 'file-detail'
    parser_classes = (MultiPartParser,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return Response({
            'tickets': reverse(TicketList.name, request=request),
            'files': reverse(FileList.name, request=request),
        })