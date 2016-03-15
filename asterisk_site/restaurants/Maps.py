#DOCUMENTATION ~ ORIGINAL (authored by Brandon Dixon)

#This file is primarily concerned with finding distance data (e.g. zipcodes,
#travel time between two pairs of lat/lng points, etc.)

import json
import requests
import googlemaps
import bs4
import re
from math import radians, cos, sin, asin, sqrt

def hsine(lat1, lon1, lat2, lon2,travel_mode = 'driving'):
    '''
    The haversine function was taken directly from http://stackoverflow.com/
    questions/4913349/haversine-formula-in-python-bearing-and-distance-between-
    two-gps-points

    For our use, we use it as a backup to the standard googleapi request. Because
    of the graph-based solution, the number of api calls increases exponentially
    with the number of restaurants/movies fed into the realm of possibilities (we
    need to calculate travel time between every node on the graph). As a result
    of the fact that this number can easily exceed the maximum number of calls
    set by Google in a day's use of the algorithm, we use a haversine function
    to first calculate the approximate distance between any given pair of
    coordinates and then a simple rate calculation to estimate the time it
    would take to travel based on the mode of transportation. 
    '''
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    #a dictionary of average rates depending on mode of transportation
    rate_dict = {'driving':40, 'walking':3.1, 'transit':30, 'bicycling': 17}

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3959 # Radius of earth in kilometers. Use 3959 for miles
    distance = c * r
    travel_speed = rate_dict[travel_mode]

    #returns estimated time of travel
    return distance / travel_speed

def travel_time(origin_lat, origin_long, dest_lat, dest_long, travel_mode='driving'):
    '''
    This function makes use of the google api to calculate the time of travel_mode
    between any pair of coordinates. Obviously because of its increased accuracy,
    we depend on this function primarily for our results, but given the limited
    number of calls we are able to make, accept the use of the Haversine 
    formula, as will be notable in the next function.
    '''
    #travel mode can take values: 'driving', 'walking', 'bicycling', and 'transit'

    api_key = 'AIzaSyDoV3acX1mSLi3V1FWT__mjIaoq5QdHlg0'
    orig_coord = str(origin_lat)+','+str(origin_long)
    dest_coord = str(dest_lat)+','+str(dest_long)
    url = "https://maps.googleapis.com/maps/api/distancematrix/" + \
          "json?units=imperial&origins=" + orig_coord + "&destinations=" \
          + dest_coord +"&mode=" + str(travel_mode) +"&key=" + api_key
    result= json.loads(requests.get(url).text)
    time = result['rows'][0]['elements'][0]['duration']['value']

    return time / 60

def get_distance(lat1, lon1, lat2, lon2, travel_mode='driving'):
    '''
    This is the function we will be using to calculate the time of travel 
    between any two given coordinate points. As already mentioned, we first try 
    and use the google api, but if that fails to cooperate, we except the 
    KeyError and return the result of the haversine formula instead
    '''
    try:
        time = travel_time(lat1, lon1, lat2, lon2, travel_mode)
    except KeyError:
        time = hsine(lat1, lon1, lat2, lon2, travel_mode)

    return time


def get_coordinates(address):
    '''
    Given an address string, this function makes use of the google api
    in order to find the coordinate pair of the location. We recognize that
    we could potentially run into the same overuse of the apikey issue as we
    realized in getting distances between pairs of these points; however, we
    do not have an alternative function as viable to implement as haversine. We
    also realize that the number of calls for this function is much fewer (just
    theatres, which we cap, and the home address). So, abuse of this function
    is not nearly as much of a fear.  
    '''
    gmaps = googlemaps.Client(key='AIzaSyDoV3acX1mSLi3V1FWT__mjIaoq5QdHlg0')
    geocode_result = gmaps.geocode(address)
    (lat, lng) = (geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng'])

    return (lat, lng)

def get_zip(home_lat, home_lng):
    '''
    Realizing that it's actually against the terms of the google api to get 
    a zip code based on a pair of coordinates yet having to base the movies
    scraper on a home zip code, we had to develop an alternative method. We 
    managed to find another site that provided address information based on
    a coordinate pair. Because of the difficulty navigating the site using
    traditional BeautifulSoup methods, we elected to use regex to find the 
    first string of the form "#####-####"(the site always outputs the zipcode 
    in this format). Testing for obscure cases, we have yet to find another
    reason to suspect this method would fail.
    '''
    lat = str(home_lat)
    lng = str(home_lng)

    url = 'http://www.melissadata.com/lookups/latlngzip4.asp?lat=' + lat + \
    '&lng=' +lng

    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.content, "html5lib")
    search = re.search('\d{5}-\d{4}',str(soup))
    
    #we only want the fist five digits of the zip code

    return search.group(0)[:5]