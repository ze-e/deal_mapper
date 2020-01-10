import json
from django.utils import timezone
from .models import Current_Property
from .models import Archived_Property
from .models import DB_Update

from .get_deals import *

import datetime

class Manage_Data:


    def update_db(self):
        '''
        Method called by periodic updater daemon (or manually via python manage.py db_update)

        1. Archives properties that are currently being displayed (stored in Current_Property db)
        2. Deletes any expired properties from the Archived_Property db (archives are stored for six years)
        3. Calls get_deals.py, which returns scraped data from our sources, returning them as a dict and json (which can be sent to Google Maps API etc)
        4. Having archvied our properties, we then delete all entries from our Current_Property db
        5. Once the Current_Property db is empty, we load our scraped data into Current_Property db
        6. We log the results of this script to a DB_Update db entry (yes I know, this logging is primitive and could use some impovement. Schedule it for Phase Two)
        '''
        database = {}
        sources = {
        'signnn':'https://signnn.com/listings/',
        'sambazis':'https://www.sambazisretailgroup.com/listings/',
        'themansourgroup':'http://www.themansourgroup.com/query_listingsNEW2.cfm?region=all&viewType=0&division=&sortBy=0&ltr=&priceMin=&priceMax=&CapRateMin=&states=&search=&CapRateMax=',
        'nnndeal':'http://nnndeal.com/nnn-properties-for-sale/',
        'snydercarlton':'http://snydercarlton.com/get_listings.cfm',
        'issenbergbritti':'http://www.issenbergbritti.com/all-listings/',
        'issenbergbritti2':'http://www.issenbergbritti.com/all-listings/page/2/',
        }

        self.archive_db()
        self.delete_expired()
        
        #database, databaseJSON = self.get_deals.get(sources)
        database = self.get_deals.get(sources)
        self.delete_db()
        self.load_db(database)
        log = DB_Update(log = self.log_text)
        log.save()

    def clearall_db(self):
    #clears ALL databases, both Current_property and Archived_Property! (Does not reset autoincrement)
        print("clearing all data . . .")
        self.log_text += "\r\n" + "clearing all data . . ."
        self.delete_db()
        self.delete_archive_db()

    def delete_archive_db(self):
    #clears our Archived_Property db

        print("deleting Archived_Property db . . .")
        self.log_text += "\r\n" + "clearing all data . . ."
        data = Archived_Property.objects.all()
        for item in data:
            print(str(item)+" deleted from archive")
            self.log_text += "\r\n" + str(item) + " deleted from archive"
            item.delete()

    def delete_expired(self):
    #searches for expired entries in our Archive_Property db and deletes them

        print("deleting expired Archived_Properties")
        self.log_text += "\r\n" + "deleting expired archived properties"
        
        data = Archived_Property.objects.all()
        for item in data:
            if item.property_archived_on <= timezone.now() - datetime.timedelta(days=365*6):
                print(item.property_name+" expired")
                self.log_text += "\r\n" + str(item) + " expired"

                item.delete()

    def delete_db(self):
    #deletes the Current_Property db

        print("deleting Current_Property db . . .")
        self.log_text += "\r\n" + "deleting Current_Property db . . ."
        data = Current_Property.objects.all()
        for item in data:
            print(str(item) + " deleted from current properties")
            self.log_text += "\r\n" + str(item) + " deleted from current properties"
            item.delete()

    #moves an item from current database into archive
    def archive_db(self):
        print("archiving Current_Property db . . .")
        self.log_text += "\r\n" + "archiving Current_Property db . . ."
        data = Current_Property.objects.all()
        for item in data:

            obj, created = Archived_Property.objects.get_or_create(property_name=item.property_name, property_description=item.property_description)
            
            if not created:
                obj.property_link = item.property_link
                obj.property_image = item.property_image
                obj.property_cap_rate = item.property_cap_rate
                obj.property_listing_price = item.property_listing_price
                obj.property_notes = item.property_notes
                try:
                    obj.save()
                    print(str(obj) + " archive data updated!")
                    self.log_text += "\r\n" + str(obj) + " archive data updated!"

                except Exception as e:
                    print(str(obj) + " archive data could not be updated...reason: " + str(e))
                    self.log_text += "\r\n" + str(obj) + " archive data could not be updated...reason: " + str(e)
            else:
                obj.property_name = item.property_name
                obj.property_source = item.property_source
                obj.property_description = item.property_description
                obj.property_link = item.property_link
                obj.property_image = item.property_image
                obj.property_cap_rate = item.property_cap_rate
                obj.property_listing_price = item.property_listing_price
                obj.property_lat = item.property_lat
                obj.property_lon = item.property_lon
                obj.property_notes = item.property_notes
                obj.property_created_on = item.property_created_on
                try:
                    obj.save()
                    print(str(obj) + " archived!")
                    self.log_text += "\r\n" + str(obj) + " archived!"
                except Exception as e:
                    print(str(prop) + " could not be archived...reason: " + str(e))
                    self.log_text += "\r\n" + str(prop) + "  could not be archived...reason: " + str(e)

                    
    #creates Current_Property db records from a database dict passed to it
    def load_db(self,database):
        print("writing data to Current_Property db . . .")
        self.log_text += "\r\n" + "writing data to Current_Property db . . ."

        for item in database:
            prop = Current_Property(
                property_name = item["name"],
                property_source = item["source"],
                property_description = item["description"],
                property_link = item["link"],
                property_cap_rate = item["cap_rate"],
                property_listing_price = item["listing_price"],
                property_lat = item["lat"],
                property_lon = item["lon"],
                property_notes = "None"
                )
            try:
                prop.property_image = item["picture"]
            except:
                prop.property_image = None

            try:
                prop.save()
                print(str(prop) + " transfered to current properties!")
                self.log_text += "\r\n" + str(prop) + " transfered to current properties!"
            except Exception as e:
                print(str(prop) + " failed to transfer to current properties...reason: " + str(e))
                self.log_text += "\r\n" + str(prop) + "  failed to transfer to current properties...reason: " + str(e)


    #loads Get_Deals, and also creates our log_text string, which we will log to our state-of-the-art log record
    def __init__(self):
        self.get_deals=Get_Deals()
        self.log_text=""
