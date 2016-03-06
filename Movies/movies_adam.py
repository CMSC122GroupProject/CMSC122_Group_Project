import bs4
import requests
import datetime
import sys
sys.path.insert(0, '/home/student/CMSC122_Group_Project/Gmaps')
import Maps

def get_url_flixster(zip_code):

    base_url = 'http://igoogle.flixster.com/igoogle/showtimes?movie=all&date='

    date = datetime.datetime.now()
    date_url = date.strftime("%Y%m%d")

    zip_url = '&postal='+str(zip_code)+'&submit=Go'

    url = base_url + date_url + zip_url

    return url

<<<<<<< HEAD
def get_movies_flixster(url):
=======
def clean_runtime(runtime):
    runtime = runtime.split()
    if runtime[0][0] == 'R':
        return None
    if len(runtime) < 3:
        if runtime[1] == 'min.':
            return int(runtime[0])
        else:
            return int(runtime[0]) * 100
    hours = int(runtime[0])
    minutes = int(runtime[2])
    return hours * 100 + minutes

def clean_starttime(start):
    pm = 1200
    if start[-2:] == 'am':
        start = start[:-2]
        pm = 0
    start = start.split(":")
    if int(start[0]) == 12:
        pm = 0
    start = int(start[0] + start[1]) + pm
    return start

def get_movies(url):
>>>>>>> ce0d4041a88947c53d71ed366c3edec9651bcab3

    '''

    #Example usage of site
    Example_url = 'http://igoogle.flixster.com/igoogle/showtimes?movie=all&date=20160303&postal=21228&submit=Go'

    Ex_dict = {Theatre_name:{address:'', movies:{A:[time_1, time_2, time_3], B:[...]}}}
    '''

    data_dict = {}

    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.content, "html5lib")

    theatres = soup.find_all('div', class_ ='theater clearfix')

    for theatre in theatres:

        name = theatre.find('a').text

        data_dict[name] = {}

        address = theatre.find('h2').find('span').text
        
        left = address.index('-') + 1
        address = address[left:]

        right = address.index('-')

        address = address[:right].strip()

        data_dict[name]['address'] = address

        data_dict[name]['movies'] = {}

        for movie in theatre.find('div', class_= 'showtimes clearfix').find_all('div', class_='showtime'):
            if movie.find('span'):            
                title = movie.find('h3').text.strip()
                
                try:
                    right = title.index('\n')
                except ValueError:
                    right = None
                title = title[:right]

                data_dict[name]['movies'][title] = {}

                run_time = movie.find('span').text
                left = run_time.rindex('-')
                run_time = run_time[left + 1:].strip()
                run_time = clean_runtime(run_time)

                data_dict[name]['movies'][title]['run_time'] = run_time

                times = movie.text.strip() + '\xa0'

                left = times.index(':', times.index('\n'))
                right = times.rindex('\xa0')
                times = times[left -1 :right]

                times = times.replace(u'\xa0', u' ')
                times = times.replace('\n', '').replace('\t', '')
                times = times.split(' ')
                times = [clean_starttime(start) for start in times]
                data_dict[name]['movies'][title]['start_times'] = times


    return data_dict

def get_url_fandango(zip_code):
    '''
    Example_url = 'http://www.fandango.com/60615_movietimes?date=3/4/2016'
    '''

    base_url = 'http://www.fandango.com/'

    url_zip = base_url + str(zip_code)


    date = datetime.datetime.now()
    date_url = date.strftime("%m/%d/%Y")

    url = url_zip + '_movietimes?date=' + data

def update_movies_fandango(movie_dict):

    return

def movie_filter(movie_dict):

    return

class movie:
    def __init__(self, name, start, run_time, theatre, lat, lng):
        self.name = name
        self.start = start
        self.run_time = run_time
        self.theatre = theatre
        self.lat = lat  
        self.lng = lng

######################################################################################################################################################
#sample input from sql query for Restaurant class oredered by name, price, rating, opening time (for the day specified by Dine_query, closing time, lat, lon
#so given this input you can run a for loop over this input and create the restaurant objects you want
[('Subway', 1, 4.615384615384615, 700, 2300, 41.8103212151066, -87.5934652661808), ('Subway', 1, 4.615384615384615, 700, 2300, 41.791407, -87.5896894), 
('Thai 55th Restaurant', 1, 3.045112781954887, 1100, 2200, 41.7950766, -87.5863406), 
('The Vegan Food Truck by Ste Martaen', 1, 4.487179487179487, 1100, 1530, 41.7805099, -87.603826), 
('Woodlawn Tap', 1, 3.658536585365854, 1030, 200, 41.795189, -87.5968939)]

class Restaurant():
    Restaurant_id = 0
    
    def __init__(self, name, price, desired_rating, opening_time, closing_time, latitude, longitiude):
        self.unique_id = Restaurant_id
        Restaurant_id += 1
        self.name = name
        self.price = price
        self.desired_rating = desired_rating
        self.opening_time = opening_time
        self.closing_time = closing_time
        self.latitude = latitude
        self.longitiude = longitiude
    


######################################################################################################################################################
#these are the "search" queries that people fill out in the form
#so from the object (which is already generated from Django) you can access the user's lon,lat, desired time to go out, transportation method desired etc

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

    

######################################################################################################################################################

def get_movie_objs(data_dict):

    movies = set([])

    for theatre in data_dict.keys():
        address = data_dict[theatre]['address']
        (lat,lng) = Maps.get_coordinates(address)
        for name in data_dict[theatre]['movies'].keys():
            run_time = data_dict[theatre]['movies'][name]['run_time']
            for time in data_dict[theatre]['movies'][name]['start_times']:
                movie_obj = movie(name, time, run_time, theatre, lat, lng)
                movies.add(movie_obj)

    return movies

def movie_filter(data_objs, user_start, user_end, user_lat, user_lng):

    filtered_movies = set([])

    for movie in data_objs:
        if movie.start > user_start and  movie.start + movie.run_time < user_end:
            filtered_movies.add(movie)

    return filtered_movies

class Node:
    def __init__(self, label):
        self.label = label
        self.edges = []
    def add_edge(self, neighbor, weight):
        self.edges.append((neighbor, weight))

def dinner_and_movie(restuarants, movies, home):

    graph = set([])

    for movie in movies:
        
        for resturarant in restuarants:
            eat_and_watch.add((resturarant, movie))



    return