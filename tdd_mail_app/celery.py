import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tdd_mail_app.settings')

app = Celery('tdd_main_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
