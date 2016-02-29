from django.shortcuts import render
from django.http import HttpResponse
from .models import Dine_query
from .forms import DineQueryForm
from .asterisk_pre_algo import dict_api, desired_output, tables, dict_what, DATABASE_FILENAME
from .asterisk_pre_algo import query_relations, query_join, query_where, query_select, prelim_assembly, prelim_algorithm, algorithm
#from  import algorithm

import sqlite3
import os
import re
#DATABASE_FILENAME = '/home/student/cs122-win-16-asudit/CMSC122_Group_Project/asterisk_site/restaurants.db'
#DATA_DIR = os.path.dirname(__file__)
#DATABASE_FILENAME = os.path.join(DATA_DIR, 'restaurants/restaurants.db')
day_dict = {'Monday': ('m_open', 'm_closed'), 'Tuesday': ('t_open', 't_closed'), 'Wednesday': ('w_open', 'w_closed'), 'Thursday': ('r_open', 'r_closed'),
                'Friday' : ('f_open', 'f_closed'), 'Saturday' : ('sat_open', 'sat_closed'), 'Sunday' : ('sun_open', 'sun_closed')}



def dine_query_list(request):
    dining_queries = Dine_query.objects.order_by('created_date')
    #print('hello')
    print('did it run')
    results = []
    for query in dining_queries:
        day = query.day
        print(day)
        times = day_dict[day]
        #lat = query.latitude
        #ssslon = query.longitude
        lon, lat = query.get_lon_lat()
        sample = {'name_id': query.name, 'price': query.price, 'rating': query.desired_rating , times[0] : query.opening_time, times[1] : query.closing_time, 
                'lat': lat, 'lon' : lon, 'preferences' : ['name_id', 'distance', 'price', 'rating', times[0], times[1] ] }
        algo = algorithm(sample)
        results.append((query, algo))
        print('it worked!!!!!!!!!!!!!' , results)
    #return results
    #return render(request, 'restaurants/dine_query_list.html', {'dining_query_results': results })

    return render(request, 'restaurants/dine_query_list.html', {'dining_query_results': results }) 

def dine_query_new(request):
    if request.method == "POST":
        form = DineQueryForm(request.POST)
        if form.is_valid():
            form.save()
            form = DineQueryForm()
    else:
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


        