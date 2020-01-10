from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .manage_data import *

from .models import Current_Property
#from django.db.models import Q
from .forms import SearchForm

from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def index(request):
	properties={}
	properties=Current_Property.objects.all()
	if request.method == 'POST':
		form=SearchForm(request.POST)

		if form.is_valid():
			if form.cleaned_data['query_name']!="" and form.cleaned_data['query_name']!=None:
				properties=properties.filter(property_name__icontains=form.cleaned_data['query_name'])  
				print("filtered name" +form.cleaned_data['query_name'])
			if form.cleaned_data['query_description']!="" and form.cleaned_data['query_description']!=None: 
				properties=properties.filter(property_description__icontains=form.cleaned_data['query_description'])  
				print("filtered desc" +form.cleaned_data['query_description'])
			if form.cleaned_data['query_cap_rate_min']!="" and form.cleaned_data['query_cap_rate_min']!=None:
				properties=properties.filter(property_cap_rate__gte=form.cleaned_data['query_cap_rate_min']) 
				print("filtered crmn" +str(form.cleaned_data['query_cap_rate_min']))
			if form.cleaned_data['query_cap_rate_max']!="" and form.cleaned_data['query_cap_rate_max']!=None:
				properties=properties.filter(property_cap_rate__lte=form.cleaned_data['query_cap_rate_max']) 
				print("filtered crmx" +str(form.cleaned_data['query_cap_rate_max']))
			if form.cleaned_data['query_listing_price_min']!="" and form.cleaned_data['query_listing_price_min']!=None: 
				properties=properties.filter(property_listing_price__gte=form.cleaned_data['query_listing_price_min']) 
				print("filtered lmn"+str(form.cleaned_data['query_listing_price_min']))
			if form.cleaned_data['query_listing_price_max']!="" and form.cleaned_data['query_listing_price_max']!=None: 				
				properties=properties.filter(property_listing_price__lte=form.cleaned_data['query_listing_price_max']) 
				print("filtered lmx"+str(form.cleaned_data['query_listing_price_max']))
			
	else:
		form=SearchForm()

	if properties==None:
		properties="None"
	else:
		propertiesJSON = serializers.serialize("json", properties)

	context={
		'title':'Current Deals:',
		'properties':properties,
		'propertiesJSON':propertiesJSON,
		'form':form
		}
	
	return render(request,'deal_mapper/index.html',context)
	