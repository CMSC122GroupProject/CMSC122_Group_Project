#DOCUMENTATION~ORIGINAL ; while clearly based on a DJANGO views.py page, 
#it has been modified beyond recognition, so we believe it qualifies as ORIGINAL script (authored by ADAM SUDIT)

from django.shortcuts import render
from django.http import HttpResponse
from .models import Dine_query
from .forms import DineQueryForm
from .query_maker import dict_api, desired_output, tables, dict_what, DATABASE_FILENAME
from .query_maker import query_relations, query_join, query_where, query_select, prelim_assembly, prelim_algorithm, algorithm
import googlemaps
from .movies import go, movie, restaurant


import sqlite3
import os
import re

day_dict = {'Monday': ('m_open', 'm_closed'), 'Tuesday': ('t_open', 't_closed'), 'Wednesday': ('w_open', 'w_closed'), 'Thursday': ('r_open', 'r_closed'),
                'Friday' : ('f_open', 'f_closed'), 'Saturday' : ('sat_open', 'sat_closed'), 'Sunday' : ('sun_open', 'sun_closed')}

def process_query(request, query):
    '''
    given a query object created by filling out the form, this function
    generates a input dictionary for the prelim-algorithm function in query_maker.py
    '''
    day = query.day
    times = day_dict[day]
    transport_method = query.transport_by
    query.get_lon_lat()
    sample = { 'price': query.price, 'rating': query.desired_rating , times[0] : query.opening_time, times[1] : query.closing_time, 
                   'lon' : query.longitude, 'lat': query.latitude  }
    return sample, times


def dine_query_list(request):
    '''
    this function is responsible for turning the input sample dictionary from the query above
    into the results displayed on the Restaurant Queries Page
    '''
    dining_queries = Dine_query.objects.order_by('created_date')
    if not dining_queries:
        return render(request, 'restaurants/dine_query_list.html', {'headers' : ['  No Query Submitted ']}) 
    else:
        query = dining_queries[0]
        print('did it run')
    
        sample, times = process_query(request, query)
        desired_output.append(times[0])
        desired_output.append(times[1])
               
        
        algo = prelim_algorithm(sample)
        
        
        for i in [times[0], times[1]]:
            desired_output.remove(i)
        
        for key in day_dict.keys():
            if (times[0], times[1]) == day_dict[key]:
                day_table = key
                break
    
        c = {'dining_query_results': list(algo), 'headers' : ['Restaurants', 'Price (1-5) ', 'Rating (1-5) ']
        ,'timing' : [day_table + ':' + " " + 'Opening Time', day_table + ':' + " "+'Closing Time' ] }

        return render(request, 'restaurants/dine_query_list.html', c)

def movies_query_list(request):
    '''
    uses the input sample dictionary generated from the first function on this page to generate
    the dinner and movie planner seen on the Asterisk Experience Page; prelim_algorithm is
    used to generate restaurant queries. This is then fed into an algorithm in movies.py that creates 
    movie-restaurant combinations. This output is then processed into HTML
    '''
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

        brandon = go(movie_output, query.opening_time, query.closing_time, query.transport_by, query.latitude, query.longitude, query.day)
        rv = 0
        longest_list = 0
        dict_movies = {}
        for entry in brandon:
            if entry[0] == 'movie':
                obj_pair = [('Event Type', entry[0]), ('name', entry[1]), ('start time', entry[2]), ('run time', entry[3]), ('theatre'), entry[4]]
                if rv not in dict_movies:
                    dict_movies[rv] = []
                
                dict_movies[rv].append(obj_pair)
            elif entry[0] == 'restaurant':
                obj_pair = [('Event Type', entry[0]), ('name', entry[1]), ('price', entry[2]), ('rating', entry[3]), ('opening_time', entry[4]),
                            ('closing_time', entry[5])]
                if rv not in dict_movies:
                    dict_movies[rv] = []
                dict_movies[rv].append(obj_pair)
            else:
                if len(dict_movies[rv]) > longest_list:
                    longest_list = len(dict_movies[rv])
                rv += 1
        movie_to_html = list(dict_movies.values())
        header_list = []
        rv = 0
        for i in range(longest_list):
            rv += 1
            header_list.append('Event' + " " + str(rv))
        rv = 0

        c = {'header_num': header_list, 'movie_row': movie_to_html}
        print(len(header_list))

        return render(request, 'restaurants/movies_query_list.html', c)


def main_page(request):
    '''
    allows the home page to be rendered by using the home page HTML template
    '''
    return render(request, 'restaurants/home_page.html')

def dine_query_new(request):
    '''
    if a request is of the type post, generates a form using the forms page HTML template;
    will then save that form into the Django generated SQL database for later use. In order
    to keep this databse tidy, I delete old queries whenever this forms page is accessed
    '''
    if request.method == "POST":
        Dine_query.objects.order_by('created_date').delete()
        form = DineQueryForm(request.POST)
        if form.is_valid():
            form.save()

            form = DineQueryForm()
    else:
        Dine_query.objects.order_by('created_date').delete()
        form = DineQueryForm()

    
    return render(request, 'restaurants/dine_query_edit.html', {'form': form})



        