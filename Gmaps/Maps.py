
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