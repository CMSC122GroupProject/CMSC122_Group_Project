
import json
import requests
import googlemaps
from math import radians, cos, sin, asin, sqrt

#just for testing
def hsine(lat1, lon1, lat2, lon2,travel_mode = 'driving'):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    rate_dict = {'driving':40, 'walking':3.1, 'transit':30}

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3959 # Radius of earth in kilometers. Use 3959 for miles
    distance = c * r
    travel_speed = rate_dict[travel_mode]
    return distance / travel_speed

def travel_time(origin_lat,origin_long,dest_lat,dest_long,travel_mode='driving'):
    #travel mode can take values: 'driving', 'walking', 'bicycling', and 'transit'
    api_key = 'AIzaSyDoV3acX1mSLi3V1FWT__mjIaoq5QdHlg0'
    orig_coord = str(origin_lat)+','+str(origin_long)
    dest_coord = str(dest_lat)+','+str(dest_long)
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + orig_coord + "&destinations=" + dest_coord +"&mode=" + str(travel_mode) +"&key=" + api_key #need to work on this
    print(url)
    result= json.loads(requests.get(url).text)
    time = result['rows'][0]['elements'][0]['duration']['value']

    return time / 60
#might need to implement cases based on "status"
#can also use "text" key to make output easier
'''
Sample json output
{
   "destination_addresses" : [ "102-110 W Barre St, Baltimore, MD 21201, USA" ],
   "origin_addresses" : [ "3101 S Western Ave, Chicago, IL 60608, USA" ],
   "rows" : [
      {
         "elements" : [
            {
               "distance" : {
                  "text" : "1,131 km",
                  "value" : 1131341
               },
               "duration" : {
                  "text" : "10 hours 31 mins",
                  "value" : 37856
               },
               "status" : "OK"
            }
         ]
      }
   ],
   "status" : "OK"
}
'''

def get_coordinates(address):

    gmaps = googlemaps.Client(key='AIzaSyDoV3acX1mSLi3V1FWT__mjIaoq5QdHlg0')
    geocode_result = gmaps.geocode(address)
    (lat, lng) = (geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng'])

    return (lat, lng)
'''
#original code; we're probably going to have an issue with the address deal. Just keep in mind
#works randomly; perhaps because of api key usage
#Wait, no, I just have bad internet right now!

#the original
def get_coordinates(address):
    
    example_url = 'http://maps.google.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=false'
    
    address = address.replace(' ', '+')

    url = 'http://maps.google.com/maps/api/geocode/json?address=' + address + '&sensor=false'
    result= json.loads(requests.get(url).text)

    (lat, lng) = (result['results'][0]['geometry']['location']['lat'], result['results'][0]['geometry']['location']['lng'])

    return (lat, lng)
'''
