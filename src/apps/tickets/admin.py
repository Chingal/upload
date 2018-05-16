from django.contrib import admin
from .models import Ticket, File

class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'ticket', )

admin.site.register(Ticket)
admin.site.register(File, FileAdmin)