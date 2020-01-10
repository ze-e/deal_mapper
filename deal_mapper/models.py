from django.db import models
from datetime import datetime
from django.utils import timezone

from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
#class Deals(models.Model):
#   created_at=models.DateTimeField(default=datetime.now,blank=True)
#makemigrations deal_mapper to place in database
#python manage.py migrate
#https://www.youtube.com/watch?v=D6esTdOLXh4&list=WL&index=4&t=1885s

class Current_Property(models.Model):
    property_name = models.CharField(max_length=200,null=True,blank=True)
    property_created_on = models.DateTimeField(auto_now_add=True)
    propety_edited_on = models.DateTimeField(auto_now=True)
    property_source = models.CharField(default="Unknown",max_length=200)
    property_description = models.TextField(default="",null=True,blank=True)
    property_link = models.URLField(default="#",null=True,blank=True)
    property_image = models.FileField(blank=True,null=True)
    property_cap_rate = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
    property_listing_price = models.PositiveIntegerField(blank=True,null=True)

    property_lat = models.DecimalField(max_digits=25, decimal_places=20,blank=True,null=True)
    property_lon = models.DecimalField(max_digits=25, decimal_places=20,blank=True,null=True)
    property_notes = models.TextField(default="None",blank=True,null=True)

    class Meta:
        verbose_name_plural = "Current Properties"
        unique_together = ("property_name","property_description")

    def __str__(self):
        return str(self.id)+": "+self.property_name + " - " +str(self.property_description) + "  "+ str(self.property_created_on)

class Archived_Property(models.Model):
    property_name = models.CharField(max_length=200,null=True,blank=True)
    property_archived_on = models.DateTimeField(auto_now_add=True)
    property_created_on = models.DateTimeField(blank=True,null=True)
    propety_edited_on = models.DateTimeField(auto_now=True)
    property_source = models.CharField(default="Unknown",max_length=200)    
    property_description = models.TextField(default="",null=True,blank=True)
    property_link = models.URLField(default="#",null=True,blank=True)
    property_image = models.FileField(blank=True,null=True)
    property_cap_rate = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
    property_listing_price = models.PositiveIntegerField(blank=True,null=True)
    property_lat = models.DecimalField(max_digits=25, decimal_places=20,blank=True,null=True)
    property_lon = models.DecimalField(max_digits=25, decimal_places=20,blank=True,null=True)
    property_notes = models.TextField(default="None",blank=True,null=True)

    class Meta:
        verbose_name_plural = "Archvied Properties"
        unique_together = ("property_name","property_description")
        default_permissions = ("delete", "view")

    def __str__(self):
        return str(self.id)+": "+self.property_name + " - " +str(self.property_description) + "  "+ str(self.property_created_on)


class DB_Update(models.Model):
    ran_on = models.DateTimeField(auto_now_add=True)
    log = models.TextField(default="None",blank=True,null=True)

    def __str__(self):
        return str(self.id)+" - " + str(self.ran_on)

    class Meta:
        default_permissions = ("view")

