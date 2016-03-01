from django.db import models
from django.utils import timezone
import geocoder

class Dine_query(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    desired_rating = models.IntegerField()
    opening_time = models.IntegerField()
    closing_time = models.IntegerField()
    day = models.CharField(max_length=10)
    distance = models.FloatField()
    current_location = models.CharField(max_length=100)
    current_city = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=timezone.now)
    longitude = None
    latitude = None


    def __repr__(self):
        return '{}: Price: {}, Desired Rating: {}, Opening Time: {}, Closing Time: {}, Distance: {}'.format(self.name, self.price, self.desired_rating, self.opening_time, self.closing_time, self.distance)

    def __str__(self):
        return '{}: Price: {}, Desired Rating: {}, Opening Time: {}, Closing Time: {}, Distance: {}'.format(self.name, self.price, self.desired_rating, self.opening_time, self.closing_time, self.distance)

    def get_lon_lat(self):
        address = self.current_location
        city = self.current_city
        g = geocoder.google(",".join(("address", "city")))
        (self.longitude, self.latitude) = g.latlng
        return self.longitude, self.latitude



        '''
        geolocator = Nominatim()
        address = self.current_location
        city = self.current_city
        location = geolocator.geocode("address" + "city")  
        (self.longitude, self.latitude) = (location.longitude, location.latitude)
        '''
