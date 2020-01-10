from django.core.management.base import BaseCommand
from deal_mapper.manage_data import *

class Command(BaseCommand):
    help = "Clears current and archived databases"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("running scheduled databse update...")
        manage_deals=Manage_Data().clearall_db()