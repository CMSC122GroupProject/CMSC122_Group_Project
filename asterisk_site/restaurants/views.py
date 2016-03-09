from django.shortcuts import render
from django.http import HttpResponse
from .models import Dine_query
from .forms import DineQueryForm
from .asterisk_pre_algo import dict_api, desired_output, tables, dict_what, DATABASE_FILENAME
from .asterisk_pre_algo import query_relations, query_join, query_where, query_select, prelim_assembly, prelim_algorithm, algorithm
import googlemaps
from .movies import go, movie, restaurant


import sqlite3
import os
import re
#DATABASE_FILENAME = '/home/student/cs122-win-16-asudit/CMSC122_Group_Project/asterisk_site/restaurants.db'
#DATA_DIR = os.path.dirname(__file__)
#DATABASE_FILENAME = os.path.join(DATA_DIR, 'restaurants/restaurants.db')
day_dict = {'Monday': ('m_open', 'm_closed'), 'Tuesday': ('t_open', 't_closed'), 'Wednesday': ('w_open', 'w_closed'), 'Thursday': ('r_open', 'r_closed'),
                'Friday' : ('f_open', 'f_closed'), 'Saturday' : ('sat_open', 'sat_closed'), 'Sunday' : ('sun_open', 'sun_closed')}

def process_query(request, query):
    day = query.day
    times = day_dict[day]
    transport_method = query.transport_by
    query.get_lon_lat()
    sample = { 'price': query.price, 'rating': query.desired_rating , times[0] : query.opening_time, times[1] : query.closing_time, 
                   'lon' : query.longitude, 'lat': query.latitude   ,'preferences' : [ 'name_id', 'distance', 'price', 'rating', times[0], times[1] ] }
    return sample, times


def dine_query_list(request):
    #dining_queries = Dine_query.objects.order_by('created_date')
    
    dining_queries = Dine_query.objects.order_by('created_date')
    if not dining_queries:
        return render(request, 'restaurants/dine_query_list.html', {'headers' : ['  No Query Submitted ']}) 
    else:
        query = dining_queries[0]
        print('did it run')
    #query = Dine_query.objects.order_by('created_date')[0]
    #print('hello')
        ###print('did it run')
    #results = []
    
    #for query in dining_queries:
        
    #assuming of course we just have one query############        
        ###day = query.day
    #print(day)
        ###times = day_dict[day]
        ###transport_method = query.transport_by
        #lat = query.latitude
        #ssslon = query.longitude
        ###query.get_lon_lat()
        #gmaps = googlemaps.Client(key='AIzaSyDoV3acX1mSLi3V1FWT__mjIaoq5QdHlg0')
        #address = query.current_location
        #city = query.current_city
        #input_loc = address, city
        #geocode_result = gmaps.geocode(input_loc)
        #query.latitude = geocode_result[0]['geometry']['location']['lat']
        #query.longitude = geocode_result[0]['geometry']['location']['lng']
        ###sample = { 'price': query.price, 'rating': query.desired_rating , times[0] : query.opening_time, times[1] : query.closing_time, 
                   ###'lon' : query.longitude, 'lat': query.latitude   ,'preferences' : [ 'name_id', 'distance', 'price', 'rating', times[0], times[1] ] }
        sample, times = process_query(request, query)
        desired_output.append(times[0])
        desired_output.append(times[1])
               
        
        algo = prelim_algorithm(sample)
        ###print(algo)
        ###desired_output.append('lat')
        ###desired_output.append('lon')
        ###movie_output = prelim_algorithm(sample)
        ###for i in ['lat', 'lon', times[0], times[1]]:
            ###desired_output.remove(i)
        
        #not in original#
        for i in [times[0], times[1]]:
            desired_output.remove(i)
        #not in orginal#
        
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
    dining_queries = Dine_query.objects.order_by('created_date')
    if not dining_queries:
        return render(request, 'restaurants/movies_query_list.html', {'headers' : ['  No Query Submitted ']}) 
    else:
        query = dining_queries[0]
        sample, times = process_query(request, query)
        desired_output.append(times[0])
        desired_output.append(times[1])
        desired_output.append('lat')
        desired_output.append('lon')
        movie_output = prelim_algorithm(sample)
        for i in [times[0], times[1],'lat', 'lon']:
            desired_output.remove(i)

        for key in day_dict.keys():
            if (times[0], times[1]) == day_dict[key]:
                day_table = key
                break

        #print(sample)
        brandon = go(movie_output, query.opening_time, query.closing_time, query.transport_by, query.latitude, query.longitude, 60615)
        rv = 0
        longest_list = 0
        dict_movies = {}
        for entry in brandon:
            if entry[0] == 'movie':
                obj = movie(entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], travel_from_home = 0, type = entry[0])
                obj_pair = [('Event Type', entry[0]), ('name', entry[1]), ('start time', entry[2]), ('run time', entry[3]), ('theatre'), entry[4]]
                if rv not in dict_movies:
                    dict_movies[rv] = []
                
                dict_movies[rv].append(obj_pair)
            elif entry[0] == 'restaurant':
                obj = restaurant(entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], type = entry[0])
                obj_pair = [('Event Type', entry[0]), ('name', entry[1]), ('price', entry[2]), ('rating', entry[3]), ('opening_time', entry[4]),
                            ('closing_time', entry[5])]
                if rv not in dict_movies:
                    dict_movies[rv] = []
                dict_movies[rv].append(obj_pair)
            else:
                print('FOUND ITTT')
                if len(dict_movies[rv]) > longest_list:
                    longest_list = len(dict_movies[rv])
                rv += 1
        movie_to_html = list(dict_movies.values())
        #for val in dict_movies.values()
            #movie_to_html.append(val)
        header_list = []
        rv = 1
        for i in range(longest_list):
            header_list.append('Event' + " " + str(rv))
            rv += 1
        rv = 0



        #print(brandon)
        #c = {'dining_query_results': list(movie_output), 'headers' : ['Restaurants', 'Price (1-5) ', 'Rating (1-5) ']
        #,'timing' : [day_table + ':' + " " + 'Opening Time', day_table + ':' + " "+'Closing Time' ] }

        c = {'header_num': header_list, 'movie_row': movie_to_html}
        print(len(header_list))

        return render(request, 'restaurants/movies_query_list.html', c)


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


        