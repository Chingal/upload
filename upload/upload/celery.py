import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upload.settings')

app = Celery('upload')

app.config_from_object('django.conf:settings')

# Si tenemos nuestras tareas en un fichero de nombre tasks.py, esto nos permite indicarle a celery que encuentre automáticamente dicho módulo dentro del proyecto. De este modo no tenemos que añadirlo a la variable CELERY_IMPORTS del settings
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Ejemplo de tarea que muestra su propia información. El bind=True indica que hace referencia a su instancia de tarea actual.
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))