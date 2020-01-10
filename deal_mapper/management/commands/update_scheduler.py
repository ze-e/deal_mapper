from django.core.management.base import BaseCommand, CommandError
import os
from crontab import CronTab

class Command(BaseCommand):
    help = 'Schedule database updating'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #init cron
        cron = CronTab(user=True)

        #add new cron job
        #change "python3" to "python" as needed
        job = cron.new(command='cd /deal_mapper/djangoproject && python manage.py update_db', comment='cronDBUpdate')

        print("scheduling db update . . .")
        #job settings
        job.setall('0 0 * * 3')
        #job.minute.every(5)

        cron.write()

        #crontab -l
        #check if cron worked