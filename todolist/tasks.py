# tasks.py
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import ToDo

def send_deadline_reminder(todo):
    subject = f"Дедлайн задачи '{todo.title}' приближается!"
    message = f"Привет, {todo.user.username}!\n\n" \
              f"Дедлайн по задаче '{todo.title}' приближается. У вас осталось меньше 1 часа до дедлайна.\n\n" \
              "Пожалуйста, завершите задачу вовремя."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [todo.user.email])

def check_deadlines():
    now = timezone.now()
    upcoming_deadline = now + timedelta(hours=1)  # Задачи, дедлайн которых меньше чем через 1 час
    todos = ToDo.objects.filter(deadline__lte=upcoming_deadline, deadline__gt=now, is_complete=False)

    for todo in todos:
        send_deadline_reminder(todo)
