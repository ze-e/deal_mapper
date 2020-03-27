from __future__ import unicode_literals
from requests import get, RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

import sys
import time
import json
import re
from django.core.serializers.json import DjangoJSONEncoder

#to add geocoding at a later date
#https://pypi.org/project/geopy/

class Get_Deals:
    '''
    1. get_properties takes each url passed to it and connects to the site using either an http request (faster), or selenium 
        (slower, but bypasses CORS errors and can scrape dynamically loaded data)

    sources({urlname : url}) -> simple_get/selenium_get 

    2. get_properties passes the http response or selenium driver to a function that processes it. Unfortunately each site has to
        be hardcoded at the moment, but perhaps in the future one function can use regex to scrape all sites

    simple_get/selenium_get -> process_url 

    3. the <url>_process functions scrapes the site. Each property it scrapes is divided into a uniform set of fields (source, name, description, link, 
        picture, cap rate, listing price, lat and lon)

    process_url -> properties[{source, name, description, link, picture, cap rate, listing price, lat, lon}]

    4. create_dict writes these fields to a dictionary. These dictionaries are returned to <url>_process, which is added to a list of properties

    propertie[{fields}] + propertie[{fields}] + ...propertie[{fields}] -> properties[{fields}]

    4. get_properties adds the properties from each site to a master list of dicts, converts this to json and returns both

    properties[{fields}] + properties[{fields}] + ...properties[{fields}] -> properties[{fields}], properties JSON

    '''
    def process_signnn(self,driver):
    #find process_signnn properties
        properties = []
        print("writing signnn properties...")

        #scroll down to make sure everything loads
        print("loading all images via scroll...")
        self.scroll_down(driver)
        print("scrolling complete!")

        content = driver.find_elements_by_class_name("inner-entry")

        for c in content:
            propertie = {}

            try:
                name = c.find_element_by_class_name("listings-heading").text.split("|")[0]
            except:
                name =  None

            try:
                link = c.find_element_by_tag_name("a").get_attribute("href")
            except:
                link = None

            try:
                picture = c.find_element_by_tag_name("img").get_attribute("src")
            except:
                picture = None

            try:    
                description = c.find_element_by_class_name("listings-description").text
            except:
                description=None


            #use some regex to get the Cap Rate. 
            #I found it was easier to just search for the "Cap Rate" string and then get rid of everything but the numbers later
            try:
                cap_rate_string = c.find_elements_by_class_name("col")[0]
                cap_rate_string = r"Cap Rate: \d+.\d+"
                    
                matches_cr = re.search(cap_rate_string,str(copy.text), re.MULTILINE)
                cap_rate = matches_cr.group().replace("Cap Rate: ","")
            except:
                cap_rate = None

            #same as above. Make sure to get rid of everything but the numbers, so we can save it to our decimal model
            try:
                listing_price_string = c.find_element_by_class_name("listings-price")
                p = r"[0-9]+(,?[0-9]+)*"
                matches_p = re.search(p, str(listing_price_string.text), re.MULTILINE)
                listing_price = matches_p.group().replace(",", "")
            except:
                listing_price = None

            source = "signnn"

            if name != None:
                properties.append(self.create_dict(source,name,link,picture,description,cap_rate,listing_price))
        
        print("signn properties: {!s}".format(properties))
        return properties


    def process_sambazis(self,response):
    #find sambazis properties
        properties = []
        print("writing sambazis properties...")
        
        if response is not None:
            site = BeautifulSoup(response, 'html.parser')
            for entry in site.find_all("div",class_ = "span-4"):

                name = entry.find("a",class_ = "title").get_text()

                link = entry.find("a",class_ = "button-link")["href"]
                if link == None:
                    link = "#"

                try:
                    picture = [img["src"] for img in entry.find_all("img",class_ = "attachment-listing-images size-listing-images wp-post-image")][0]       
                except:
                    picture = None

                description = entry.find("p",class_ = "listings-city-state-zip").get_text()

                cap_rate_section = [dd for dd in entry.find_all("dd")]
                cap_rate_string = cap_rate_section[1].get_text()

                c = r"\d+.\d+"
                matches_c = re.search(c,str(cap_rate_string), re.MULTILINE)

                if matches_c != None:
                    cap_rate = matches_c.group()
                else:
                    cap_rate = None

                listing_price_string = entry.find("dd",class_ = "price").get_text()

                p = r"[0-9]+(,?[0-9]+)*"
                matches_p = re.search(p, str(listing_price_string), re.MULTILINE)

                if matches_p != None:
                    listing_price = matches_p.group().replace(",", "")
                else:
                    listing_price = None

                source = "sambazis"

                if name != None:
                    properties.append(self.create_dict(source,name,link,picture,description,cap_rate,listing_price))

        else:
            return None

        print("sambazis properties: {!s}".format(properties))
        return properties

    def process_themansourgroup(self,response):
    #find themansourgroup properties
        properties = []
        print("writing themansourgroup properties...")
        
        if response is not None:
            site = BeautifulSoup(response, 'html.parser')
            for entry in site.find_all("div",class_ = "propertyholder"):    

                link_a = [a["href"] for a in entry.find_all("a")]
                try:
                    link = link_a[0]
                except:
                    link = "#"
            
                picDiv = entry.find("div",class_ = "imageHolder")
                try:
                    picture = [img["src"] for img in picDiv.find_all("img")][0]
                except:
                    picture = None
                
                info = [propInfo for propInfo in entry.find_all("div",class_ = "propInfoListing")]
                name = info[0].find("strong").get_text()
                description = str(info[1]).split('>')[1].split('<')[0]
                
                price_block = [price for price in entry.find_all("div",class_ = "priceBlock")]
                price_block = str(price_block[0]).split('>')

                try:
                    listing_price_string = price_block[3].split('<')[0]

                    p = r"[0-9]+(,?[0-9]+)*"
                    matches_p = re.search(p, str(listing_price_string), re.MULTILINE)
                    listing_price = matches_p.group().replace(",", "")

                except:
                    listing_price = None

                try:
                    cap_rate_string = price_block[6].split('<')[0]

                    c = r"\d+.\d+"
                    matches_c = re.search(c,str(cap_rate_string), re.MULTILINE)
                    cap_rate = matches_c.group()

                except:
                    cap_rate = None

                source = "themansourgroup"
                if name != None:
                    properties.append(self.create_dict(source,name,link,picture,description,cap_rate,listing_price))

        else:
            return None

        print("themansourgroup properties: {!s}".format(properties))
        return properties

    def process_nnndeal(self,driver):
    #find nnndeal properties
        properties = []
        print("writing nnndeal properties...")

        #scroll down to make sure everythiong loads
        print("loading all info via scroll...")
        self.scroll_down(driver)
        print("scrolling complete!")

        content = driver.find_elements_by_tag_name("article")

        for c in content:
            propertie = {}

            try:
                name = c.find_element_by_class_name("tg-element-1").find_element_by_tag_name("a").text
            except:
                name = None

            try:
                link = c.find_element_by_tag_name("a").get_attribute("href")
            except:
                link = None

            try:
                picture_string = c.find_element_by_class_name("tg-item-image").get_attribute("style")
                picture = str(picture_string).split("(")[1].split(")")[0].strip('\"')
            except:
                picture = None

            try:    
                description = c.find_element_by_class_name("tg-element-5").text
            except:
                description=None

            try:
                cap_rate_string = c.find_element_by_class_name("tg-element-3").text                 
                cap_rate = cap_rate_string.replace("%","")
            except:
                cap_rate = None

            try:
                listing_price_string = c.find_element_by_class_name("tg-element-2").text
                listing_price = listing_price_string.replace(",", "").replace("$", "")
            except:
                listing_price = None

            source = "nnndeal"
            if name != None:
                properties.append(self.create_dict(source,name,link,picture,description,cap_rate,listing_price))

        
        print("nnndeal properties: {!s}".format(properties))
        return properties


    def process_snydercarlton(self,resp):
    #find snydercarlton properties
        properties = []
        print("writing snydercarlton properties...")
        if resp is not None:
            site = BeautifulSoup(resp, 'html.parser')
            for entry in site.find_all("div",class_ = "property"):
                propertie = {}
                try:
                    picture = [img["src"] for img in entry.find_all("img")][0]
                except:
                    picture = None
                
                link_a = [a["href"] for a in entry.find_all("a")]
                try:
                    link = link_a[0]
                except:
                    link = "#"

                info = str(entry.find("span",class_="blackText14")).split("<")
                name = info[1].split(">")[1]
                description = info[2].split(">")[1]

                prices = str(entry.find("div",{"align":"center"}))

                p = r"Price: \$[0-9]+(,?[0-9]+)*"
                matches_p = re.search(p, str(prices), re.MULTILINE)

                if matches_p != None:
                    listing_price = matches_p.group().replace(",", "")
                    listing_price = listing_price.split("$")[1]
                else:
                    listing_price = None

                c = r"Cap Rate: \d+.\d+"
                matches_c = re.search(c,str(prices), re.MULTILINE)

                if matches_c != None:
                    cap_rate = matches_c.group().replace("Cap Rate: ","")
                else:
                    cap_rate = None

                source = "snydercarlton"

                if name != None:
                    properties.append(self.create_dict(source,name,link,picture,description,cap_rate,listing_price))
        else:
            return None
        
        print("snydercarlton properties: {!s}".format(properties))

        return properties


    def process_issenbergbritti(self,resp):
    #find issenbergbritti properties
        properties = []
        print("writing issenbergbritti properties...")
        if resp is not None:
            site = BeautifulSoup(resp, 'html.parser')
            for entry in site.find_all("div",class_ = "item-wrap"):
                propertie = {}

                link_a = [a for a in entry.find_all("a")]

                try:
                    name = link_a[1].get_text()
                except:
                    name = None

                try:
                    link = link_a[0]["href"]
                except:
                    link = "#"  

                try:
                    picture = [img["src"] for img in entry.find_all("img")][0]
                except:
                    picture = None

                try:
                    description = entry.find("address", class_ = "property-address").get_text()
                except:
                    description = None 
               
                #cap rate is not listed on this site
                cap_rate = None

                try:
                    listing_price_string = entry.find("span",class_ = "item-price item-price-text").get_text()

                    p = r"[0-9]+(,?[0-9]+)*"
                    matches_p = re.search(p, str(listing_price_string), re.MULTILINE)
                    listing_price = matches_p.group().replace(",", "")
                except:
                    listing_price = None


                source = "issenbergbritti"
            
                if name != None:
                    properties.append(self.create_dict(source,name,link,picture,description,cap_rate,listing_price))

        else:
            return None
        
        print("issenbergbritti properties: {!s}".format(properties))

        return properties


    def process_issenbergbritti_pg2(self,resp):
    #find issenbergbritti pg2 properties
        properties = []
        print("writing issenbergbritti pg2 properties...")
        if resp is not None:
            site = BeautifulSoup(resp, 'html.parser')
            for entry in site.find_all("div",class_ = "item-wrap"):
                propertie = {}
                
                link_a = [a for a in entry.find_all("a")]

                try:
                    name = link_a[1].get_text()
                except:
                    name = None

                try:
                    link = link_a[0]["href"]
                except:
                    link = "#"  

                try:
                    picture = [img["src"] for img in entry.find_all("img")][0]
                except:
                    picture = None

                #cap rate is not listed on this site
                cap_rate = None

                description = entry.find("address",class_="property-address")

                try:
                    listing_price_string = entry.find("span",class_="item-price item-price-text").get_text()

                    p = r"[0-9]+(,?[0-9]+)*"
                    matches_p = re.search(p, str(listing_price_string), re.MULTILINE)
                    listing_price = matches_p.group().replace(",", "")
                except:
                    listing_price = None

                source = "issenbergbritti2"
            
                if name != None:
                    properties.append(self.create_dict(source,name,link,picture,description,cap_rate,listing_price))

        else:
            return None
        
        print("issenbergbritti2 properties: {!s}".format(properties))

        return properties

    def check_response(self,resp):
    #a helper function to check if the content is html, returns false otherwise

        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 
            and content_type is not None)

    def simple_get(self,url):
    #makes a get request to url, checks if it is html/xml and returns an error if it is not

        print("making get request...")
        try:
            with closing(get(url, stream = True)) as resp:
                if self.check_response(resp):
                    return resp.content
                else:
                    print('connection error','Site returned errorcode {!s}'.format(resp.status_code))
                    return None

        except RequestException as error:
            print('connection error','Error requesting url {0} : {1!s}'.format(url, error))
            return None

    def selenium_get(self,url):
    #use selenium to load page, in order to scrape dynamically loaded info (ie from ajax)
    
        if sys.platform.startswith("linux"):
            try:
                options = webdriver.ChromeOptions()
                options.add_argument("headless")
                driver = webdriver.Chrome(DRIVER_FOLDER,chrome_options=options)
            except WebDriverException:
                print("Webriver exception. Please install Chrome browser with the correct version of Chrome webdriver. View documentation for further instructions.")
                return None
            except Exception as error:
                print("Error starting Selenium {0!s} --e".format(error))
                return None  
        #windows
        elif sys.platform.startswith("win32"):
            try:
                options = webdriver.ChromeOptions()
                options.add_argument("headless")
                driver = webdriver.Chrome(DRIVER_FOLDER,chrome_options=options)
            except WebDriverException:
                print("Webriver exception. Please install Chrome browser with the correct version of Chrome webdriver. View documentation for further instructions.")
                return None
            except Exception as error:
                print("e-- {0!s} --e".format(error))
                return None

        else:
            print("os not supported. Please use windows or linux")
            return None

        try:
            print("connected successfully")
            driver.get(url)
            return driver

        except RequestException as error:
            print('connection error','Error requesting url {0} : {1!s}'.format(url, error))
            return None

        except Exception as error:
            print("Error starting Selenium {0!s} --e".format(error))
            return None 

    def scroll_down(self,driver):
    #a selenium helper function that scrolls down the page to allow all data to load

        current_scroll = driver.execute_script("return window.pageYOffset")
        bottom_scroll = driver.execute_script(" return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight) - window.innerHeight;")   
        while current_scroll != bottom_scroll:
            driver.execute_script("window.scrollBy(0, 1000);")

            time.sleep(2)
            current_scroll = driver.execute_script("return window.pageYOffset")
            print("scrolling...{0!s} of {1!s}".format(current_scroll, bottom_scroll))

    def create_dict(self,source,name,link,picture,description,cap_rate,listing_price):
        propertie = {}
        propertie["source"] = source
        propertie["link"] = link
        propertie["picture"] = picture
        propertie["name"] = name
        propertie["description"] = description
        propertie["cap_rate"] = cap_rate
        propertie["listing_price"] = listing_price
        #lat and lon are for placing the property on a google map. You must use a geocoder and place the numbers here later
        propertie["lat"] = None
        propertie["lon"] = None

        return propertie

    def get_properties(self,sources):
    #find properties per each url, and add them to the properties list. Returns list of dicts and json
        print("reading urls...")
        properties = []

        if "signnn" in sources:
            print("getting properties from signnn...")
            driver = self.selenium_get(sources["signnn"])
            if driver:
                properties.extend(self.process_signnn(driver))
            else:
                print("error connecting to {}".format(sources["signnn"]))

        if "sambazis" in sources:
            print("getting properties from sambazis...")
            response = self.simple_get(sources["sambazis"])
            if response:
                properties.extend(self.process_sambazis(response))
            else:
                print("error connecting to {}".format(sources["sambazis"]))

        if "themansourgroup" in sources:
            print("getting properties from themansourgroup...")
            response = self.simple_get(sources["themansourgroup"])
            if response:
                properties.extend(self.process_themansourgroup(response))
            else:
                print("error connecting to {}".format(sources["themansourgroup"]))

        if "nnndeal" in sources:
            print("getting properties from nnndeal...")
            driver = self.selenium_get(sources["nnndeal"])
            if driver:
                properties.extend(self.process_nnndeal(driver))
            else:
                print("error connecting to {}".format(sources["nnndeal"]))

        if "snydercarlton" in sources:
            print("getting properties from snydercarlton...")
            response = self.simple_get(sources["snydercarlton"])
            if response:
                properties.extend(self.process_snydercarlton(response))
            else:
                print("error connecting to {}".format(sources["url"]))

        if "issenbergbritti" in sources:
            print("getting properties from issenbergbritti...")
            response = self.simple_get(sources["issenbergbritti"])
            if response:
                properties.extend(self.process_issenbergbritti(response))
            else:
                print("error connecting to {}".format(sources["issenbergbritti"]))

        if "issenbergbritti2" in sources:
            print("getting properties from issenbergbritti2...")
            response = self.simple_get(sources["issenbergbritti2"])
            if response:
                properties.extend(self.process_issenbergbritti_pg2(response))
            else:
                print("error connecting to {}".format(sources["issenbergbritti2"]))

        #clean up and return our properties
        driver.quit()
        propertiesJSON = json.dumps(list(properties), cls = DjangoJSONEncoder)

        return properties, propertiesJSON


    def get(self, sources):
    #wrapper for get_properties

        return self.get_properties(sources)
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 
            and content_type is not None)

    def simple_get(self,url):
    #makes a get request to url, checks if it is html/xml and returns an error if it is not

        print("making get request...")
        try:
            with closing(get(url, stream = True)) as resp:
                if self.check_response(resp):
                    return resp.content
                else:
                    print('connection error','Site returned errorcode {!s}'.format(resp.status_code))
                    return None

        except RequestException as error:
            print('connection error','Error requesting url {0} : {1!s}'.format(url, error))
            return None

    def selenium_get(self,url):
    #use selenium to load page, in order to scrape dynamically loaded info (ie from ajax)

        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        if sys.platform.startswith("linux"):
            driver = webdriver.Chrome(chrome_options=options)
        else:
            driver = webdriver.Chrome("./chromedriver.exe",chrome_options=options)
        
        #nonheadless driver for testing
        #driver = webdriver.Chrome()

        try:
            print("connected successfully")
            driver.get(url)
            return driver
        except RequestException as error:
            print('connection error','Error requesting url {0} : {1!s}'.format(url, error))
            return None

    def scroll_down(self,driver):
    #a selenium helper function that scrolls down the page to allow all data to load

        current_scroll = driver.execute_script("return window.pageYOffset")
        bottom_scroll = driver.execute_script(" return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight) - window.innerHeight;")   
        while current_scroll != bottom_scroll:
            driver.execute_script("window.scrollBy(0, 1000);")

            time.sleep(2)
            current_scroll = driver.execute_script("return window.pageYOffset")
            print("scrolling...{0!s} of {1!s}".format(current_scroll, bottom_scroll))

    def create_dict(self,source,name,link,picture,description,cap_rate,listing_price):
        propertie = {}
        propertie["source"] = source
        propertie["link"] = link
        propertie["picture"] = picture
        propertie["name"] = name
        propertie["description"] = description
        propertie["cap_rate"] = cap_rate
        propertie["listing_price"] = listing_price
        #lat and lon are for placing the property on a google map. You must use a geocoder and place the numbers here later
        propertie["lat"] = None
        propertie["lon"] = None

        return propertie

    def get_properties(self,sources):
    #find properties per each url, and add them to the properties list. Returns list of dicts and json
        print("reading urls...")
        properties = []

        if "signnn" in sources:
            print("getting properties from signnn...")
            driver = self.selenium_get(sources["signnn"])
            if driver:
                try:
                    properties.extend(self.process_signnn(driver))
                except:
                    print("Couldn't get properties from signnn")
                    pass
            else:
                print("error connecting to {}".format(sources["signnn"]))

        if "sambazis" in sources:
            print("getting properties from sambazis...")
            response = self.simple_get(sources["sambazis"])

            if response:
                try:
                    properties.extend(self.process_sambazis(response))
                except:
                    print("Couldn't get properties from sambazis")
                    pass
            else:
                print("error connecting to {}".format(sources["sambazis"]))

        if "themansourgroup" in sources:
            print("getting properties from themansourgroup...")
            response = self.simple_get(sources["themansourgroup"])
            if response:
                try:
                    properties.extend(self.process_themansourgroup(response))
                except:
                    print("Couldn't get properties from themansourgroup")
                    pass
            else:
                print("error connecting to {}".format(sources["themansourgroup"]))

        if "nnndeal" in sources:
            print("getting properties from nnndeal...")
            driver = self.selenium_get(sources["nnndeal"])
            if driver:
                try:
                    properties.extend(self.process_nnndeal(driver))
                except:
                    print("Couldn't get properties from nnndeal")
                    pass
            else:
                print("error connecting to {}".format(sources["nnndeal"]))

        if "snydercarlton" in sources:
            print("getting properties from snydercarlton...")
            response = self.simple_get(sources["snydercarlton"])

            if response:
                try:
                    properties.extend(self.process_snydercarlton(response))
                except:
                    print("Couldn't get properties from snydercarlton")
                    pass
            else:
                print("error connecting to {}".format(sources["snydercarlton"]))

        if "issenbergbritti" in sources:
            print("getting properties from issenbergbritti...")
            response = self.simple_get(sources["issenbergbritti"])
            if response:
                try:
                    properties.extend(self.process_issenbergbritti(response))
                except:
                    print("Couldn't get properties from issenbergbritti")
                    pass
            else:
                print("error connecting to {}".format(sources["issenbergbritti"]))

        if "issenbergbritti2" in sources:
            print("getting properties from issenbergbritti2...")
            response = self.simple_get(sources["issenbergbritti2"])
            if response:
                try:
                    properties.extend(self.process_issenbergbritti_pg2(response))
                except:
                    print("Couldn't get properties from issenbergbritti2")
                    pass
            else:
                print("error connecting to {}".format(sources["issenbergbritti2"]))

        #clean up and return our properties
        #driver.quit()
        #propertiesJSON = json.dumps(list(properties), cls = DjangoJSONEncoder)

        #return properties, propertiesJSON
        return properties



    def get(self, sources):
    #wrapper for get_properties

        return self.get_properties(sources)
