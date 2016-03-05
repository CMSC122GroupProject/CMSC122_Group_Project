from django import forms
from .models import Dine_query

class DineQueryForm(forms.ModelForm):
    

    class Meta:
        model = Dine_query
        #fields = ('name', 'price', 'desired_rating', 'opening_time', 'closing_time', 'day', 'distance', 'current_location', 'current_city')
        
        fields = ( 'price', 'desired_rating', 'opening_time', 'closing_time', 'day', 'current_location', 'current_city', 'transport_by')
        #tank = forms.IntegerField(widget=forms.HiddenInput(), initial=123)
    
    '''
    price = forms.IntegerField(widget=forms.HiddenInput(), initial=5)
    desired_rating = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    opening_time = forms.IntegerField(widget=forms.HiddenInput(),initial=600)
    closing_time = forms.IntegerField(widget=forms.HiddenInput(),initial=2400)
    day = forms.CharField(widget=forms.HiddenInput(),max_length=10)
    distance = forms.FloatField(widget=forms.HiddenInput())
    current_location = forms.CharField(widget=forms.HiddenInput(),max_length=100)
    current_city = forms.CharField(widget=forms.HiddenInput(),max_length=20)
    '''