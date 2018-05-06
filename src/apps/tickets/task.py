from celery.task import task
from celery import shared_task

@shared_task
def SaveImage(obj, Photo):
    if Photo.objects.filter(ticket=obj.ticket).count() >= obj.ticket.limit:
        obj.ticket.status = 'CLOSE'
        obj.ticket.save()
        return
    obj.ticket.num_photos = obj.ticket.num_photos + 1
    obj.ticket.save()