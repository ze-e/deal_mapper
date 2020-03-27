#https://www.valentinog.com/blog/drf/

from rest_framework import serializers
from .models import Current_Property

class Current_Property_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Current_Property
        fields = ('property_name', 'property_created_on', 'propety_edited_on', 'property_source','property_description','property_link','property_image','property_cap_rate','property_listing_price','property_lat','property_lon','property_notes')