from django.core.management.base import BaseCommand
from deal_mapper.manage_data import *

class Command(BaseCommand):
    help = "Updates the database with newly scraped information"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("running scheduled databse update...")
        manage_deals=Manage_Data().update_db()