# tasks.py
from celery import shared_task
from .models import ToDo
from datetime import datetime

@shared_task
def delete_expired_todos():
    now = datetime.now()
    ToDo.objects.filter(expiration_time__lte=now).delete()