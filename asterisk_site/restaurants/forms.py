from django import forms
from .models import Dine_query

class DineQueryForm(forms.ModelForm):

    class Meta:
        model = Dine_query
        fields = ('name', 'price', 'desired_rating', 'opening_time', 'closing_time', 'day', 'distance')
