from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """ Definition UserSerializer from User model and specific fields """
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        #Token.objects.create(user=user)
        return user

class TicketSerializer(serializers.ModelSerializer):
    """ Definition TicketSerializer from Ticket model and specific fields """
    class Meta:
        model = Ticket
        fields = ('id', 'number', 'limit', 'num_photos', 'status', 'user', )

class PhotoSerializer(serializers.ModelSerializer):
    """ Definition PhotoSerializer from Photo model and specific fields """
    class Meta:
        model = Photo
        fields = ('id', 'ticket', 'image', )