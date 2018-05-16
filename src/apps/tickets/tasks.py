import os
import boto3
from celery import task, shared_task
from django.conf import settings
from .constants import IN_PROGRESS, COMPLETED 
from .models import Ticket, File
BUCKET = settings.AWS_STORAGE_BUCKET_NAME

@shared_task
def add(x,y):
    return (x+y)

@shared_task()
def Upload(path, id):
    ticket = Ticket.objects.get(id=id)
    file_count = ticket.get_file_count
    if file_count < ticket.limit:
        ticket.status = IN_PROGRESS
        with open(path, 'rb') as f:
            data = f.read()    
        filebase = os.path.basename(path)    
        upload_path = 'upload/{}/{}'.format(ticket.user.username, filebase)    
        File.objects.create(ticket=ticket, file=upload_path)
        s3 = boto3.resource('s3')
        s3.Object(BUCKET, upload_path).put(Body=data)
        if (file_count+1) == ticket.limit:
            ticket.status = COMPLETED
        ticket.save()
        f.close()        
    os.remove(path)    
    return True