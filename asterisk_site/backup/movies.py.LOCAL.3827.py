#DOCUMENTATION~ORIGINAL (authored by Ken Jung and Brandon Dixon)

#This file handes all of the movie implementation of our project. From scraping
#the websites to algorthmically selecting an optimal restaurant-movie schedule.

import bs4
import requests
import datetime
import sys
import queue
from Maps import get_distance, hsine, get_coordinates, travel_time, get_zip
#took away . from .Maps

def later(time_start, time_added):
    '''
    Because all times are written in military, we devise this function to add
    time (in minutes) to any given start time (for example, we may want to add 
    105 minutes to a time_start of 800. This function would yield the time 945
    as the result).
    '''
    min_per_hr = 60
    hours_add = time_added // min_per_hr
    min_add = time_added % min_per_hr
    time_end = time_start + (100 * hours_add) + min_add
    return time_end

def get_url_flixster(zip_code, day_of_week):
    '''
    Generates a url for flixster so we can scrape movietimes and locations. The 
    url requires just a home zipcode, which we generate from the get_zip function 
    on Maps.py
    '''

    days_of_week = {'Sunday': 7, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
                 'Thursday': 4, 'Friday': 5, 'Saturday': 6}
    base_url = 'http://igoogle.flixster.com/igoogle/showtimes?movie=all&date='
    #use datetime to get the current date of the call
    date = datetime.datetime.now()
    today_of_week = date.isoweekday()
    days_until_desire = days_of_week[day_of_week] - today_of_week
    days_until_desire = min(days_until_desire + 7, days_until_desire)
    date_url = date + datetime.timedelta(days=days_until_desire)
    date_url = date_url.strftime("%Y%m%d")
    zip_url = '&postal='+str(zip_code)+'&submit=Go'
    url = base_url + date_url + zip_url
    return url

def get_url_fandango(zip_code, day_of_week):
    '''
    Find the url corresponding to the zip code and today's day of the week 
    for movie showtimes
    '''
    days_of_week = {'Sunday': 7, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
                 'Thursday': 4, 'Friday': 5, 'Saturday': 6}
    base = 'http://www.fandango.com/'
    end = '_movietimes?date='
    #use datetime to get the current date of the call
    date = datetime.datetime.now()
    today_of_week = date.isoweekday()
    days_until_desire = days_of_week[day_of_week] - today_of_week
    days_until_desire = min(days_until_desire + 7, days_until_desire)
    date_url = date + datetime.timedelta(days=days_until_desire)
    date_url = date_url.strftime("%m/%d/%Y")
    return base + str(zip_code) + end + date_url

def scrub_runtime(runtime):
    '''
    Conform the runtime of the film to military time duration
    '''
    run = runtime[2:-1]
    run = run.split('H')
    run = [int(r) for r in run]
    return run[0] * 100 + run[1]

def scrub_starttime(starttime):
    '''
    Conform the start time of the movie to 24hr military time
    '''
    start = starttime.split('T')[1]
    start = start.split('-')[0]
    time = start.split(':')
    hour = time[0]
    minute = time[1]
    time = hour + minute
    return int(time)

def get_movies_fandango(url, theatre_max = 3):
    '''
    Scrape fandango for movies given the url. Output to a dictionary.
    '''
    theatre_count = 1
    data_dict = {}
    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.content, "html5lib")
    theatres = soup.find_all('div', itemtype = 'http://schema.org/MovieTheater')
    for theatre in theatres:
        if theatre_count <= theatre_max:
            name = theatre.find(itemprop = 'name')['content']
            data_dict[name] = {}
            address_info = theatre.find('span', itemprop = 'address')
            street = address_info.find(itemprop = 'streetAddress' )['content']
            city = address_info.find(itemprop = 'addressLocality' )['content']
            zipcode = address_info.find(itemprop = 'postalCode' )['content']
            state = address_info.find(itemprop = 'addressRegion' )['content']
            data_dict[name]['address'] = street + ' ' + city + ', ' + state + ' ' + zipcode
            data_dict[name]['movies'] = {}
            movies = theatre.find_all('span', itemprop = 'event')
            if movies:
                for movie in movies:
                    title = movie.find(itemprop = 'name')['content']
                    runtime = movie.find(itemprop = 'duration')['content']
                    runtime = scrub_runtime(runtime)
                    if runtime == 0:
                        pass
                    data_dict[name]['movies'][title] = {}
                    data_dict[name]['movies'][title]['run_time'] = runtime
                    start_times = movie.find_all(itemprop = 'startDate')
                    starting = []
                    for start in start_times:
                        s = scrub_starttime(start['content'])
                        starting.append(s)
                    data_dict[name]['movies'][title]['start_times'] = starting
            theatre_count += 1

    return data_dict

def clean_runtime(runtime):
    '''
    Same function as scrub_runtime, but customized to handle Fandango's runtimes 
    '''
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
    '''
    Same function as scrub_starttime, but customized to handle Fandango's runtimes 
    '''
    pm = 1200
    if start[-2:] == 'am':
        start = start[:-2]
        pm = 0
    start = start.split(":")
    
    if int(start[0]) == 12:
        pm = 0
    if len(start) < 2:
        return start

    start = int(start[0] + start[1]) + pm
    return start

def get_movies_flixster(url, theatre_max = 3):
    '''
    Retrieves flixster's movie showtimes for the given url
    Example usage of site
    Example_url = 'http://igoogle.flixster.com/igoogle/showtimes?movie=all&date=20160303&postal=21228&submit=Go'

    Ex_dict = {Theatre_name:{address:'', movies:{A:[time_1, time_2, time_3], B:[...]}}}
    '''

    data_dict = {}

    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.content, "html5lib")

    theatres = soup.find_all('div', class_ ='theater clearfix')
    theatre_count = 1
    for theatre in theatres:
        if theatre_count <= theatre_max:
            name = theatre.find('a').text

            data_dict[name] = {}

            address = theatre.find('h2').find('span').text
            
            left = address.index('-') + 1
            address = address[left:]

            right = address.index('-')

            address = address[:right].strip()

            data_dict[name]['address'] = address

            data_dict[name]['movies'] = {}
            if theatre.find('div', class_= 'showtimes clearfix'):
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
                        times = times.split(' ') #might be an issue
                        
                        times = [clean_starttime(start) for start in times]
                        
                        data_dict[name]['movies'][title]['start_times'] = times
            theatre_count += 1

    return data_dict

def get_all_movies(zipcode, day_of_week):
    '''
    Invokes both movie scraper functions based on today's day of the week and a given zipcode
    to return a giant dictionary of all theaters and films.

    Double-counting of movie theaters is only possible if the same theater is spelled 
    differently in Fandango than in Flixster (e.g. 'Carmikes' vs. 'Carmike's')
    '''
    fan = get_movies_fandango(get_url_fandango(zipcode, day_of_week))
    flix = get_movies_flixster(get_url_flixster(zipcode, day_of_week))
    for k in flix:
        fan[k] = flix[k]
    return fan

class Home:
    def __init__(self,lat,lng, name='home'):
        self.lat = lat
        self.lng = lng
        self.name = 'home'

class movie:
    def __init__(self, name, start, run_time, theatre, lat, lng, travel_from_home=0, type = 'movie'):
        self.name = name
        self.start = start
        self.run_time = run_time
        self.theatre = theatre
        self.lat = lat  
        self.lng = lng
        self.travel_from_home = travel_from_home
        self.type = 'movie' 

class restaurant:
    def __init__(self, name, price, rating, opening_time, closing_time, lat, lng, type = 'restaurant'):
        self.name = name
        self.price = price
        self.rating = rating
        self.opening_time = opening_time
        self.lat = lat
        self.lng = lng
        if closing_time < 500:
            self.closing_time = 2400
        else:
            self.closing_time = closing_time
        self.type = "restaurant"    

def get_movie_objs(data_dict, home, user_start, user_end, travel_mode = 'driving'):

    movies = set([])

    theatre_count = 0

    for theatre in data_dict.keys():
        #if theatre_count < theatre_max:
         #   theatre_count += 1
        address = data_dict[theatre]['address']
        (lat,lng) = get_coordinates(address)
        travel_time = get_distance(home.lat, home.lng,lat, lng, travel_mode)
        if user_start + travel_time < user_end:
            for name in data_dict[theatre]['movies'].keys():
                run_time = data_dict[theatre]['movies'][name]['run_time']
                for time in data_dict[theatre]['movies'][name]['start_times']:
                    if run_time != None:
                        if time > user_start and  time + run_time < user_end:
                            movie_obj = movie(name, time, run_time, theatre, lat, lng, travel_time)
                            movies.add(movie_obj)

    return movies

def get_restaurant_objs(restaurants):

    rest_objs = set([])

    for rest in restaurants:
        name = rest[0]
        price = rest[1]
        rating = rest[2]
        opening_time = rest[3]
        closing_time = rest[4]
        lat = rest[5]
        lng = rest[6]
        new_rest = restaurant(name, price, rating, opening_time, closing_time, lat, lng)
        rest_objs.add(new_rest)

    return rest_objs

class Node:
    def __init__(self, data, efficiency = 0, efficient_neighbor = None):
        self.data = data
        self.edges = []
        self.efficiency = efficiency
    def add_edge(self, neighbor, weight):
        self.edges.append((neighbor, weight))

def get_graph(restaurants, movies, home, travel_mode = 'driving'):

    graph = []

    home = Node(home)
    
    #weight originally just set to the time of travel
    for movie in movies:
        show = Node(movie)
        home.add_edge(show, show.data.travel_from_home) #did we do this?
        
        for node in graph:
            #move to movie?
            if node.data.type != 'movie':
                travel = get_distance(node.data.lat, node.data.lng, movie.lat, movie.lng, travel_mode)
                node.add_edge(show,travel)
                show.add_edge(node, travel)

        graph.append(show)

    for restaurant in restaurants:
        eat = Node(restaurant)
        home.add_edge(eat, get_distance(home.data.lat, home.data.lng, restaurant.lat, restaurant.lng, travel_mode))

        for node in graph:
            if node.data.type != 'restaurant':
                travel = get_distance(node.data.lat, node.data.lng, restaurant.lat, restaurant.lng, travel_mode)
                node.add_edge(eat,travel)
                eat.add_edge(node, travel)

        graph.append(eat)

    return (home,graph)

def filter_data(time, end_time, edges, eating_time = 45):

    possible_edges = set([])

    for node in edges:
        if node[0].data.type == 'movie':
            #can you make it to see the start and can you make it to see the end?
            arrival = time + node[1]
            end_of_movie = later(node[0].data.start, node[0].data.run_time)
            if arrival <= node[0].data.start and end_of_movie < end_time:    
                possible_edges.add((end_of_movie,node))
        elif node[0].data.type == 'restaurant':
            arrival = later(time, node[1])
            end_of_eating = later(arrival, eating_time)
            #check to see you arrive after it's open, end eating before its closed, and end eating before time is up
            if arrival > node[0].data.opening_time and end_of_eating < node[0].data.closing_time and end_of_eating < end_time:
                possible_edges.add((end_of_eating, node))

    return possible_edges

def movie_and_dinner_algo(graph, home_node, start_time, end_time, efficiency = 0, eating_time = 45):

    sol_dict = {}

    possible_nodes = filter_data(start_time, end_time, home_node.edges)

    if possible_nodes == set([]):
        return sol_dict #or something else
    else:
        for node in possible_nodes:
            if node[1][0].data.type == 'movie': 
                efficiency += node[1][0].data.run_time
            elif node[1][0].data.type == 'restaurant':
                efficiency += eating_time
            if node[1][0].efficiency < efficiency:
                index = graph.index(node[1][0])
                graph[index] = node[1][0]
                sol_dict[node[1][0]] = movie_and_dinner_algo(graph, node[1][0], node[0], end_time, efficiency, eating_time)

        return sol_dict

def get_solutions(sol_dict, output_4_adam = []):

    if sol_dict == {}:
        output_4_adam.append('FLAG')
    else:
        for node in sol_dict.keys():
            if node.data.type == 'movie':
                new_tup = (node.data.type, node.data.name, node.data.start, node.data.run_time, node.data.theatre,node.data.lat,node.data.lng)
            if node.data.type == 'restaurant':
                new_tup = (node.data.type, node.data.name, node.data.price, node.data.rating, node.data.opening_time,node.data.closing_time,node.data.lat, node.data.lng) 
            output_4_adam.append(new_tup)
            get_solutions(sol_dict[node], output_4_adam)

    return output_4_adam



def go(restaurant_list, user_start, user_end, travel_mode, user_lat, user_lng,
         day_of_week):

    home = Home(user_lat, user_lng)
    user_zip = get_zip(user_lat, user_lng)
    movie_data = get_all_movies(user_zip, day_of_week)
    movie_objs = get_movie_objs(movie_data, home, user_start, user_end, travel_mode)
    rest_objs = get_restaurant_objs(restaurant_list)
    (home_node, graph_of_travels) = get_graph(rest_objs, movie_objs, home, travel_mode)
    sol_dict = movie_and_dinner_algo(graph_of_travels, home_node, user_start, user_end)
    output = get_solutions(sol_dict)
    return output 
