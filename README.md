
## Installation:

1. Install python3

2. Install requirements.txt

3. Install Google Chrome

https://linuxize.com/post/how-to-install-google-chrome-web-browser-on-ubuntu-18-04/

or

`sudo apt-get install google-chrome-stable`

4. Create a superuser to access the admin panel

-note: if you can't find manage.py, make sure you are in the file `deal_mapper/djangoproject` !

LINUX ONLY!

5. Install Chromedriver

-note : the chromedriver is unfortunately a source of many headaches. Try following the directions here:
https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/

6. Install python-crontab:

`pip install python-crontab`

7. Start the automated weekly updater

`manage.py update_scheduler`

### Source sites

Currently six sites are being scraped:

'signnn':'https://signnn.com/listings/'

'sambazis':'https://www.sambazisretailgroup.com/listings/'

'themansourgroup':'http://www.themansourgroup.com/'

'nnndeal':'http://nnndeal.com/nnn-properties-for-sale/'

'snydercarlton':'http://snydercarlton.com/get_listings.cfm'

'issenbergbritti':'http://www.issenbergbritti.com/all-listings/'
(this is split into two sites in the code, one for each page)

If development continues, more sites will be added, including:

http://www.nnnpro.com/:

https://srsre.com/

https://trivanta.com/

http://www.jamescapitaladvisors.com/listings

http://www.matthews.com/

### manage.py commands

When all dependencies have loaded and the site is running, there are some helpful commands you can run from the commandline. These are custom commands executed with manage.py (https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/):

`update_db` - moves the current_property database to the archived_property database and updates current_property database

`clearall_db` - deletes all properties from current_property and archived_property databases\

`test_get_deals` - runs the webscraper, but DOES NOT write the data to the database

`update_scheduler` - runs update_db automatically once weekly (MUST have python-crontab installed) LINUX ONLY! (Note - make sure that you use the command "python" and not "python3." Otherwise you must edit line 17 of update_scheduler.py in the folder deal_mapper/djangoproject/deal_mapper/management/commands

### model

All scraped properties are written to the fields:

Source - the site the property was scraped from (ie signnn, sambazis)

Name/Keyword - the main/heading title of the property listing. Usually the type of property (ie Walgreens, Autozone) but might    
    contain other information depending on the format of the source site

Link - uri to detail page of the property listing from the source

Picture - the image of the property listing

Description - the subheading of the property listing. Usuaully the address or location of the property (ie 1234 Fake Street, 
    Texas; CVS - GrandRapids) but might contain other information depending on the format of the source site

Cap Rate - cap rate as a decimal (ie 4.5 , 3.75)

Listing Price - listing price as an integer (ie 10500, 20000)

Lat - used for geocoding. When scraped from the site, it's initial value is "None." Must be populated later from a geocoder such 
    as Google Maps API

Lon - used for geocoding. When scraped from the site, it's initial value is "None." Must be populated later from a geocoder such 
    as Google Maps API
