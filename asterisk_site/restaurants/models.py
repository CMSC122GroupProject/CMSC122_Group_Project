#DOCUMENTATION~MODIFIED: page generated from Django, and class construction code based on code from Gustav and DjangoGirls tutorial
#syntx in lon-lat method from google api documentation
#--->altered as to fit this specific project 

from django.db import models
from django.utils import timezone
from datetime import date

import googlemaps


class Dine_query(models.Model):
    
    transport_choices = [('driving', 'driving'), ('walking', 'walking'), ('bicycling', 'bicycling'), ('transit', 'transit')]
    day_choices = [( 'Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), 
                    ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')]
    num_choices = [(1,1), (2,2), (3,3), (4,4), (5,5)]


    price = models.IntegerField(choices=num_choices)
    desired_rating = models.IntegerField(choices=num_choices)
    opening_time = models.IntegerField()
    closing_time = models.IntegerField()
    day = models.CharField(choices=day_choices, max_length =15)
    current_location = models.CharField(max_length=100)
    current_city = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=timezone.now)
    terms = models.CharField(max_length=150)
    longitude = None
    latitude = None
    transport_by = models.CharField(choices=transport_choices, max_length=15)

        
    def get_lon_lat(self):
        '''
        Given the user's input address from the query object generated from the form, this 
        function will use the Google Maps api to create corresponding longitude and latitude
        '''
        gmaps = googlemaps.Client(key='AIzaSyDoV3acX1mSLi3V1FWT__mjIaoq5QdHlg0')
        address = self.current_location
        city = self.current_city
        input_loc = address, city
        geocode_result = gmaps.geocode(input_loc)
        self.latitude = geocode_result[0]['geometry']['location']['lat']
        self.longitude = geocode_result[0]['geometry']['location']['lng']

        

