#DOCUMENTATION~MODIFIED-directly based on GUSTAV and DjangoGirl tutorial, customized for our project

from django import forms
from .models import Dine_query

class DineQueryForm(forms.ModelForm):
    

    class Meta:
        model = Dine_query


        
        fields = ( 'price', 'desired_rating', 'opening_time', 'closing_time', 'day', 'terms', 'current_location', 'current_city', 'transport_by')
        
    