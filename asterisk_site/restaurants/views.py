from django.shortcuts import render
from django.http import HttpResponse
from .models import Dine_query
from .forms import DineQueryForm
#from  import algorithm

import sqlite3
import os
import re
DATABASE_FILENAME = '/home/student/cs122-win-16-asudit/CMSC122_Group_Project/asterisk_site/restaurants.db'

def dine_query_list(request):
    dining_queries = Dine_query.objects.order_by('created_date')

    return render(request, 'restaurants/dine_query_list.html', {'dining_queries': dining_queries })

def dine_query_new(request):
    if request.method == "POST":
        form = DineQueryForm(request.POST)
        if form.is_valid():
            form.save()
            form = DineQueryForm()
    else:
        form = DineQueryForm()

    
    return render(request, 'restaurants/dine_query_edit.html', {'form': form})

def dine_query_algo(request):
    dining_queries = Dine_query.objects.order_by('created_date')
    for query in dining_queries:
        sample = {'name_id': query.name, 'price': query.price, 'lon': 1.5, 'lat': 30, 'rating': query.desired_rating , 'm_open' : 3000, 'm_closed' : 2100, 
                'preferences' : ['name_id', 'distance', 'price', 'rating', 'm_open', 'm_closed' ] }
