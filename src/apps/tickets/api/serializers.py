from rest_framework import serializers
from django.contrib.auth.models import User
from apps.tickets.models import Ticket, File

class TicketSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()
    class Meta:
        model = Ticket
        fields = ('url', 'user', 'limit', 'status', 'files', )
    
    def get_user(self, obj):
        return obj.user.username
    
    def get_files(self, obj):
        files = obj.files.all()
        return FileSerializer(files, many=True).data


class FileSerializer(serializers.ModelSerializer):
    ticket = serializers.SlugRelatedField(queryset=Ticket.objects.all(), slug_field='id')
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = File
        fields = ('file', 'ticket', )

    def get_file(self, obj):
        try:
            image = obj.file.url
        except:
            image = None
        return image