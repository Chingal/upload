from django.db import models
from django.core.validators import MinValueValidator

OPEN = '0'
CLOSE = '1'

class Ticket(models.Model):
    STATUS_TYPE = (
        (OPEN, 'OPEN'),
        (CLOSE, 'CLOSE'),
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE) #Foreign Key - User
    limit = models.IntegerField(validators=[MinValueValidator(1)])  # Limit greater than or equal to 1
    status = models.CharField(max_length=10, choices=STATUS_TYPE, default=OPEN)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return "Ticket: {}".format(self.id)


class File(models.Model):
    def generate_path(instance, filename):
        return '/'.join(['upload', instance.ticket.user.username, filename])

    ticket = models.ForeignKey(Ticket, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=generate_path)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if File.objects.filter(ticket=self.ticket).count() >= self.ticket.limit:
            self.ticket.status = CLOSE
            self.ticket.save()
            return
        super(File, self).save(*args, **kwargs)

    def __str__(self):
        return "File: {}".format(self.id)