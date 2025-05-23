from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zibal.settings')

app = Celery('zibal')


app.config_from_object('django.conf:settings',)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
