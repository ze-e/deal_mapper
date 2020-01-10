from django.core.management.base import BaseCommand, CommandError
import os
from crontab import CronTab

class Command(BaseCommand):
    help = 'Disable scheduled database updating'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        deleteScheduled = int(input("Are you SURE you want to turn off scheduled database updating? Enter 1 to proceed: "))
        if deleteScheduled == 1:
            print("Deleting scheduled db update . . .")
            cron = CronTab(user=True)
            cron.remove_all()
            cron.write()
            print("Scheduled db updating has been disabled. Use command \"manage.py db_update_scheduler\" to re-enable")

        else:
            print("Did NOT turn off scheduled database updating")
