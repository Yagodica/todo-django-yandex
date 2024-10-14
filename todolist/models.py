from django.db import models

class ToDo(models.Model):
    title = models.CharField('Название задания', max_length=500)
    description = models.TextField('Описание задания', blank=True, null=True)
    deadline = models.DateTimeField('Дедлайн задания', blank=True, null=True)
    is_complete = models.BooleanField('Завершено', default=False)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title
