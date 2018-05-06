from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
import os
from .task import *

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Ticket(models.Model):
    """ The Ticket model with the fields """
    STATUS_TYPE = (
        ('OPEN', 'OPEN'),
        ('CLOSE', 'CLOSE'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Foreign Key - User
    number = models.CharField(max_length=254, blank=True, unique=True, editable=False)
    limit = models.IntegerField(validators=[MinValueValidator(1)]) # Limit greater than or equal to 1
    num_photos = models.IntegerField(default=0, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_TYPE, default='OPEN')
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return "Ticket: {} - User: {}".format(self.number, self.user)

    def save(self, *args, **kwargs):
        if len(self.number)==0:
            self.number = str(uuid.uuid4().fields[-1])[:5] # Generate unique id
        super(Ticket, self).save(*args, **kwargs)


class Photo(models.Model):
    """ The Photo model with the fields """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='upload')
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return "{} - {}".format(self.image, self.ticket.number)

    def save(self, *args, **kwargs):
        #SaveImage.delay(self, Photo)
        if Photo.objects.filter(ticket=self.ticket).count() >= self.ticket.limit:
            self.ticket.status = 'CLOSE'
            self.ticket.save()
            return
        self.ticket.num_photos = self.ticket.num_photos + 1
        self.ticket.save()
        super(Photo, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        #os.unlink(self.image.url)
        self.ticket.num_photos = self.ticket.num_photos - 1
        if self.ticket.num_photos < self.ticket.limit:
            self.ticket.status = 'OPEN'
        self.ticket.save()
        super(Photo, self).delete(*args, **kwargs)