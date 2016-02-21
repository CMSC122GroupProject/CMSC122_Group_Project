
import json
import requests

def travel_time(origin_lat,origin_long,dest_lat,dest_long,travel_mode='driving'):
    #travel mode can take values: 'driving', 'walking', 'bicycling', and 'transit'
    orig_coord = str(origin_lat)+','+str(origin_long)
    dest_coord = str(dest_lat)+','+str(dest_long)
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins="+orig_coord+"&destinations="+dest_coord+"&mode="+travel_mode+"&language=en-EN&sensor=false"
    result= json.loads(requests.get(url).text)
    driving_time = result['rows'][0]['elements'][0]['duration']['value']

    return driving_time