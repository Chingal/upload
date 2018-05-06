import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upload.settings')

app = Celery('upload')

app.config_from_object('django.conf:settings')

# Si tenemos nuestras tareas en un fichero de nombre tasks.py, esto nos permite indicarle a celery que encuentre automáticamente dicho módulo dentro del proyecto.
# De este modo no tenemos que añadirlo a la variable CELERY_IMPORTS del settings
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    BROKER_URL = 'redis://127.0.0.1:6379/0',
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0',
)