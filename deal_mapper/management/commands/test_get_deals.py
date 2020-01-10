from django.core.management.base import BaseCommand
from deal_mapper.get_deals import *

class Command(BaseCommand):
    help = "tests get_deals.py"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("running scheduled databse update...")

        #set sources
        sources = {
        'signnn':'https://signnn.com/listings/',
        'sambazis':'https://www.sambazisretailgroup.com/listings/',
        'themansourgroup':'http://www.themansourgroup.com/query_listingsNEW2.cfm?region=all&viewType=0&division=&sortBy=0&ltr=&priceMin=&priceMax=&CapRateMin=&states=&search=&CapRateMax=',
        'nnndeal':'http://nnndeal.com/nnn-properties-for-sale/',
        'snydercarlton':'http://snydercarlton.com/get_listings.cfm',
        'issenbergbritti':'http://www.issenbergbritti.com/all-listings/',
        'issenbergbritti2':'http://www.issenbergbritti.com/all-listings/page/2/',
        }

        database, databaseJSON = Get_Deals().get(sources)
        if database:
            print("get_deals ran successfully")