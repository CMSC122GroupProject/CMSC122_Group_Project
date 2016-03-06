from django.db import models
from django.utils import timezone
from datetime import date

my_date = date.today()
#from .googlemaps import geocoding, Client
import googlemaps
#from client import places_nearby
#from.client import Client
#from .places import places_nearby

class Dine_query(models.Model):
    #name = models.CharField(max_length=64)
    '''
    price = models.IntegerField()
    desired_rating = models.IntegerField()
    opening_time = models.IntegerField(default = 600)
    closing_time = models.IntegerField(default = 2400)
    
    day = models.CharField(max_length=10)
    distance = models.FloatField()
    current_location = models.CharField(max_length=100)
    current_city = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=timezone.now)
    longitude = None
    latitude = None
    '''
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


    def __repr__(self):
        return '{}: Price: {}, Desired Rating: {}, Opening Time: {}, Closing Time: {}, Distance: {}'.format( self.price, self.desired_rating, 
            self.opening_time, self.closing_time, self.distance)

    #def __str__(self):
        #return '{}: Price: {}, Desired Rating: {}'.format( self.price, self.desired_rating)

        
    def get_lon_lat(self):
        gmaps = googlemaps.Client(key='AIzaSyDoV3acX1mSLi3V1FWT__mjIaoq5QdHlg0')
        address = self.current_location
        city = self.current_city
        input_loc = address, city
        geocode_result = gmaps.geocode(input_loc)
        self.latitude = geocode_result[0]['geometry']['location']['lat']
        self.longitude = geocode_result[0]['geometry']['location']['lng']

        
        '''
        address = self.current_location
        city = self.current_city
        g = geocoder.google(",".join(("address", "city")))
        (self.longitude, self.latitude) = g.latlng
        return self.longitude, self.latitude
        '''


        '''
        geolocator = Nominatim()
        address = self.current_location
        city = self.current_city
        location = geolocator.geocode("address" + "city")  
        (self.longitude, self.latitude) = (location.longitude, location.latitude)
        '''

