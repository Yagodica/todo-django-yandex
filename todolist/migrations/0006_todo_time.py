# Generated by Django 5.1.1 on 2024-10-14 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0005_remove_todo_duedate_remove_todo_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время задания'),
        ),
    ]
