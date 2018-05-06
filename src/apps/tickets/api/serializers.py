from rest_framework import serializers
from django.contrib.auth.models import User
from apps.tickets.models import Ticket, File


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    files = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='file-detail')

    class Meta:
        model = Ticket
        fields = ('url', 'limit', 'status', 'user', 'created_at', 'files', )


class FileSerializer(serializers.HyperlinkedModelSerializer):
    ticket = serializers.SlugRelatedField(queryset=Ticket.objects.all(), slug_field='id')

    class Meta:
        model = File
        fields = ('url', 'file', 'ticket', )
