from os import environ
from celery import Celery

environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')

app = Celery('school_management')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()