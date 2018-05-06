import boto3
from celery import task
from django.conf import settings

BUCKET = settings.AWS_STORAGE_BUCKET_NAME

@task(blind=True)
def Upload(file, user):
    s3 = boto3.resource('s3')
    s3.Object(BUCKET, 'upload/{}/{}'.format(user,file.name)).put(Body=file.read())
    return True