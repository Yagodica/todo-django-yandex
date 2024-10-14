from django.db import models
from django.contrib.auth.models import User

class ToDo(models.Model):
    title = models.CharField('Название задания', max_length=500)
    description = models.TextField('Описание задания', blank=True, null=True)
    deadline = models.DateTimeField('Дедлайн задания', blank=True, null=True)
    is_complete = models.BooleanField('Завершено', default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title
