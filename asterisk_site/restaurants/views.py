from django.shortcuts import render
from django.http import HttpResponse
from .models import Dine_query
from .forms import DineQueryForm
from .asterisk_pre_algo import dict_api, desired_output, tables, dict_what, DATABASE_FILENAME
from .asterisk_pre_algo import query_relations, query_join, query_where, query_select, prelim_assembly, prelim_algorithm, algorithm
import googlemaps


import sqlite3
import os
import re
#DATABASE_FILENAME = '/home/student/cs122-win-16-asudit/CMSC122_Group_Project/asterisk_site/restaurants.db'
#DATA_DIR = os.path.dirname(__file__)
#DATABASE_FILENAME = os.path.join(DATA_DIR, 'restaurants/restaurants.db')
day_dict = {'Monday': ('m_open', 'm_closed'), 'Tuesday': ('t_open', 't_closed'), 'Wednesday': ('w_open', 'w_closed'), 'Thursday': ('r_open', 'r_closed'),
                'Friday' : ('f_open', 'f_closed'), 'Saturday' : ('sat_open', 'sat_closed'), 'Sunday' : ('sun_open', 'sun_closed')}


def dine_query_list(request):
    #dining_queries = Dine_query.objects.order_by('created_date')
    
    dining_queries = Dine_query.objects.order_by('created_date')
    if not dining_queries:
        return render(request, 'restaurants/dine_query_list.html', {'headers' : ['  No Query Submitted ']}) 
    else:
        query = dining_queries[0]
    
    #query = Dine_query.objects.order_by('created_date')[0]
    #print('hello')
        print('did it run')
    #results = []
    
    #for query in dining_queries:
        
    #assuming of course we just have one query############        
        day = query.day
    #print(day)
        times = day_dict[day]
        transport_method = query.transport_by
        #lat = query.latitude
        #ssslon = query.longitude
        query.get_lon_lat()
        #gmaps = googlemaps.Client(key='AIzaSyDoV3acX1mSLi3V1FWT__mjIaoq5QdHlg0')
        #address = query.current_location
        #city = query.current_city
        #input_loc = address, city
        #geocode_result = gmaps.geocode(input_loc)
        #query.latitude = geocode_result[0]['geometry']['location']['lat']
        #query.longitude = geocode_result[0]['geometry']['location']['lng']
        sample = { 'price': query.price, 'rating': query.desired_rating , times[0] : query.opening_time, times[1] : query.closing_time, 
                   'lon' : query.longitude, 'lat': query.latitude   ,'preferences' : [ 'name_id', 'distance', 'price', 'rating', times[0], times[1] ] }
        desired_output.append(times[0])
        desired_output.append(times[1])
               
        
        algo = prelim_algorithm(sample)
        print(algo)
        desired_output.append('lat')
        desired_output.append('lon')
        movie_output = prelim_algorithm(sample)
        for i in ['lat', 'lon', times[0], times[1]]:
            desired_output.remove(i)
        for key in day_dict.keys():
            if (times[0], times[1]) == day_dict[key]:
                day_table = key
                break
    
        c = {'dining_query_results': list(algo), 'headers' : ['Restaurants', 'Price (1-5) ', 'Rating (1-5) ']
        ,'timing' : [day_table + ':' + " " + 'Opening Time', day_table + ':' + " "+'Closing Time' ] }
        #print(movie_output)
        #results.append(algo)
    #return results
    #return render(request, 'restaurants/dine_query_list.html', {'dining_query_results': results })

        return render(request, 'restaurants/dine_query_list.html', c) 

def movies_query_list(request):
    return render(request, 'restaurants/movies_query_list.html')

def main_page(request):
    return render(request, 'restaurants/home_page.html')

def dine_query_new(request):
    if request.method == "POST":
        Dine_query.objects.order_by('created_date').delete()
        form = DineQueryForm(request.POST)
        if form.is_valid():
            form.save()
            #Dine_query.objects.order_by('created_date').delete()

            form = DineQueryForm()
            #form = DineQueryForm(initial = {'price': 5, 'desired_rating': 1, 'opening_time': 600, 'closing_time': 2400})
    else:
        Dine_query.objects.order_by('created_date').delete()
        #form = DineQueryForm(initial = {'price': 5, 'desired_rating': 1, 'opening_time': 600, 'closing_time': 2400})
        form = DineQueryForm()

    
    return render(request, 'restaurants/dine_query_edit.html', {'form': form})
'''
def dine_query_algo(request):
    dining_queries = Dine_query.objects.order_by('created_date')
    print('did it run')
    results = []
    for query in dining_queries:
        day = query.day
        times = day_dict[day]
        sample = {'name_id': query.name, 'price': query.price, 'rating': query.desired_rating , times[0] : query.opening_time, times[1] : query.closing_time, 
                'preferences' : ['name_id', 'distance', 'price', 'rating', times[0], times[1] ] }
        algo = algorithm(sample)
        results.append((query, algo))
        print(results)
    #return results
    return render(request, 'restaurants/dine_query_list.html', {'dining_query_results': results })

'''


        