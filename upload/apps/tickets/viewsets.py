import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .serializers import *
from .models import *

class TicketFilter(django_filters.FilterSet):
    """ Definition of the TicketFilter which allows filtering by specific dates """
    class Meta:
        model = Ticket
        fields = {
            'created': ['lt', 'gt', 'exact', 'year__gt'],
        }


class UserViewSet(viewsets.ModelViewSet):
    """ Definition of the UserViewset with post and get """
    queryset = User.objects.filter(is_superuser=0).order_by('id') # Filtering all different users of super admin and ordered by id
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', ]
    filter_backends = [SearchFilter]
    search_fields = ['=username'] # Search exactly by username


class TicketViewSet(viewsets.ModelViewSet):
    """ Definition of the TicketViewset with post and get """
    serializer_class = TicketSerializer
    http_method_names = ['get', 'post', ]
    filter_class = TicketFilter

    def get_queryset(self):
        user = self.request.user # Current User
        return Ticket.objects.filter(user=user).order_by('id') # Filter tickets by current user and ordered by id


class PhotoViewSet(viewsets.ModelViewSet):
    """ Definition of the PhotoViewSet with post and get """
    queryset = Photo.objects.all().order_by('id')
    serializer_class = PhotoSerializer
    http_method_names = ['get', 'post', ]