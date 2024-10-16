# management/commands/check_deadlines.py
from django.core.management.base import BaseCommand
from todolist.tasks import check_deadlines

class Command(BaseCommand):
    help = 'Check for tasks with upcoming deadlines and send reminder emails.'

    def handle(self, *args, **kwargs):
        check_deadlines()
        self.stdout.write(self.style.SUCCESS('Successfully sent reminders for upcoming deadlines.'))
