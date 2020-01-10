from django import forms

class SearchForm(forms.Form):
    
    query_name = forms.CharField(label="Keyword:",max_length=100,required=False)
    query_description = forms.CharField(label="Description:",required=False)
    query_cap_rate_max = forms.DecimalField(label="Cap Rate Max:",max_digits=5, decimal_places=2,required=False)
    query_cap_rate_min = forms.DecimalField(label="Cap Rate Min:",max_digits=5, decimal_places=2,required=False)
    query_listing_price_max = forms.IntegerField(label="Listing Price Max:",required=False)
    query_listing_price_min = forms.IntegerField(label="Listing Price Min:",required=False)   