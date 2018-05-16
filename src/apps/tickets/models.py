from django.db import models
from django.core.validators import MinValueValidator
from .constants import PENDING, STATUS_TYPE


class Ticket(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE) #Foreign Key - User
    limit = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    status = models.CharField(max_length=15, choices=STATUS_TYPE, default=PENDING)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "Ticket: {} - User: {}".format(self.id, self.user.username)
    
    @property
    def get_file_count(self):
        return self.files.all().count()


class File(models.Model):
    def generate_upload_path(instance, filename):
        return '/'.join(['upload', instance.ticket.user.username, filename])

    ticket = models.ForeignKey(Ticket, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=generate_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "Image: {} - Ticket: {}".format(self.id, self.ticket.id)