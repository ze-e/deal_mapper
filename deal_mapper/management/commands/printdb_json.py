from django.core.management.base import BaseCommand
from deal_mapper.manage_data import *

class Command(BaseCommand):
    help = "Prints current properties to json file"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("printing to json...")
        manage_deals=Manage_Data().printdb_json()