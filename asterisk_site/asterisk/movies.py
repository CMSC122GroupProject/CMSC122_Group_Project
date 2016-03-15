#DOCUMENTATION~ORIGINAL (authored by Ken Jung and Brandon Dixon)

#This file handes all of the movie implementation of our project. From scraping
#the websites to algorthmically selecting an optimal restaurant-movie schedule.

import bs4
import requests
import datetime
import sys
import queue
from .Maps import get_distance, hsine, get_coordinates, travel_time, get_zip
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
    on Maps.py, and the day of the week the user wishes to plan their journey
    '''

    #dictionary assigning a number to each day of the week
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

    #gets the number of days between now and the user's desired day of the week
    days_until_desire = days_of_week[day_of_week] - today_of_week

    #if days_until_desire is negative (for instance planning a Tuesday evening
    # on a Sunday, then add 7 days to get the number of days between the two)
    days_until_desire = min(days_until_desire + 7, days_until_desire)

    #finally, use the timedelta method to add days
    date_url = date + datetime.timedelta(days=days_until_desire)

    #output the date in the format for the url
    date_url = date_url.strftime("%Y%m%d")

    zip_url = '&postal='+str(zip_code)+'&submit=Go'
    url = base_url + date_url + zip_url
    return url

def get_url_fandango(zip_code, day_of_week):
    '''
    Find the url corresponding to the zip code and today's day of the week 
    for movie showtimes

    We scrape from both flixster and fandango (together, they have both major
    theatres in Hyde Park: Harper and Doc Films), so we perform the exact 
    same get_url function for fandango, using fandango's url style 
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

    The runtime output for the movie scrapes comes in the form "x hours and y 
    minutes." Obviously, this isn't very helpful for our purposes, so we use 
    this function to scrub the runtime strings into integers representing
    the number of minutes for a movie's runtime.
    '''
    run = runtime[2:-1]
    run = run.split('H')
    run = [int(r) for r in run]
    return run[0] * 100 + run[1]

def scrub_starttime(starttime):
    '''
    Conform the start time of the movie to 24hr military time

    Similarly to the runtime output, the starttime is also stored as a not-so-
    useful string. We use this function to store the movie starttime as a string
    representing each movie's starttime in military form
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
    Note, we limit the theatre count to just 3. This dramatically cuts down on the 
    computation of the algorithm, and does not take away the legitimacy of our 
    solution (theatres after the first three were often far away or rather
    insignificant)
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
    Once again, we limit the theatre count to just 3 for reasons explained
    above. Flixster provided us the immense benefit of speed (the site is
    practically plaitext); however, this speed came at a cost of consistency.
    You will notice the scrape for this site is messy, and we apologize for the 
    any difficulties in reading over it.
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
                        times = times.split(' ')
                        
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
    '''
    A simple class to represent the home location, which is defined merely
    as a set of coordinate points. We also save the name of the class for 
    ease in future functions
    '''
    def __init__(self,lat,lng, name='home'):
        self.lat = lat
        self.lng = lng
        self.name = 'home'

class movie:
    '''
    Another rather simple class that encapsulates all of our data we have
    surrounding each movie. Note, we store travel_from_home data in this class 
    but not in the restaurant class due to the nature of developing these 
    objects (e.g. all movies in the same theatre are the same distance from
    home, so it's easier to caclulate this value once and store it for each 
    object).
    '''
    def __init__(self, name, start, run_time, theatre, lat, lng, 
                                            travel_from_home=0, type = 'movie'):            
        self.name = name
        self.start = start
        self.run_time = run_time
        self.theatre = theatre
        self.lat = lat  
        self.lng = lng
        self.travel_from_home = travel_from_home
        self.type = 'movie' 

class restaurant:
    '''
    Class to encapsulate all the data surrounding the restaurant. This is 
    entirely based on the output produced from the initial querying the 
    database, which is why the representation may appear so similar.
    '''
    def __init__(self, name, price, rating, opening_time, closing_time, lat, lng, 
                                                            type = 'restaurant'):
        self.name = name
        self.price = price
        self.rating = rating
        self.opening_time = opening_time
        self.lat = lat
        self.lng = lng
        #due to constraints inherent in the data/algorithm, we set all restaurants
        #closing between midnight and 5 am to have a closing time of 2400.
        #this eases the process of comparing times (e.g. 2300 < 2400 but
        #2300 !< 200, despite the fact that it is for our purposes).
        if closing_time < 500:
            self.closing_time = 2400
        else:
            self.closing_time = closing_time
        self.type = "restaurant"    

def get_movie_objs(data_dict, home, user_start, user_end, travel_mode = 'driving'):
    '''
    Takes our dictionary of movie data and converts it to a set of 
    movie objects
    '''
    movies = set([])

    for theatre in data_dict.keys():
        address = data_dict[theatre]['address']
        (lat,lng) = get_coordinates(address)
        travel_time = get_distance(home.lat, home.lng,lat, lng, travel_mode)
        if later(user_start, travel_time) < user_end:
            for name in data_dict[theatre]['movies'].keys():
                run_time = data_dict[theatre]['movies'][name]['run_time']
                for time in data_dict[theatre]['movies'][name]['start_times']:
                    if run_time != None:
                        if time > user_start and  later(time, run_time) < user_end:
                            movie_obj = movie(name, time, run_time, theatre, lat, lng, travel_time)
                            movies.add(movie_obj)

    return movies

def get_restaurant_objs(restaurants):
    '''
    Takes our list of restaurant tuples from the original SQL database output
    and converts it to a set of restaurant objects.
    '''
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
    '''
    Node class to be used to represent a graph. Each node contains a data
    attribute (just the restaurant/movie class), edges--which is represented as
    a list of tuples with the first entry being the node to which you can travel
    from this node and the second entry being the time it takes to travel from
    your current node to this neighbor node--and efficiency, set to 0 for the 
    time being but is used extensively in the algorithm.
    '''
    def __init__(self, data, efficiency = 0):
        self.data = data
        self.edges = []
        self.efficiency = efficiency
    def add_edge(self, neighbor, weight):
        self.edges.append((neighbor, weight))

def get_graph(restaurants, movies, home, travel_mode = 'driving'):
    '''
    Foremost, we put the home into a node. Then the function takes our set of 
    restaurant and movie objects, and connects them first to a edge going from 
    home to each location (you can travel directly from home to any location). 
    It then connects the node to every other node in the graph of opposite class 
    (to cut down on computation, we assume the user does not want to watch back-
    to-back movies or eat back-to-back meals). It then appends the current node
    to the graph (just a list of nodes) and repeats the process until all movies
    and restaurants are exhausted. Returns a tuple with the home node as the 
    first entry and the graph as the second.
    '''
    graph = []

    home = Node(home)
    
    for movie in movies:
        show = Node(movie)
        home.add_edge(show, show.data.travel_from_home)
        
        for node in graph:
            if node.data.type != 'movie':
                travel = get_distance(node.data.lat, node.data.lng, movie.lat, 
                                                         movie.lng, travel_mode)
                node.add_edge(show,travel)
                show.add_edge(node, travel)

        graph.append(show)

    for restaurant in restaurants:
        eat = Node(restaurant)
        home.add_edge(eat, get_distance(home.data.lat, home.data.lng, 
                                   restaurant.lat, restaurant.lng, travel_mode))

        for node in graph:
            if node.data.type != 'restaurant':
                travel = get_distance(node.data.lat, node.data.lng, 
                                    restaurant.lat, restaurant.lng, travel_mode)
                node.add_edge(eat,travel)
                eat.add_edge(node, travel)

        graph.append(eat)

    return (home,graph)

def filter_data(time, end_time, edges, eating_time = 45):
    '''
    This is a helper function for the movie_and_dinner_algo function. Basically,
    it takes a current time and all possible maneuvers from the current node and
    filters the possibilities for those that would put the user over the end of 
    their allotted schedule. So, we output a set of tuples representing legitmate
    candidates. The first entry representing the time at the end of that 
    activity, and the second entry being the node itself.
    '''
    possible_edges = set([])

    for edge in edges:
        node = edge[0]
        travel_time = edge[1]
        if node.data.type == 'movie':
            #can you make it to see the start and can you make it to see the end?
            arrival = later(time, travel_time)
            end_of_movie = later(node.data.start, node.data.run_time)
            if arrival <= node.data.start and end_of_movie < end_time:    
                possible_edges.add((end_of_movie,node))
        elif node.data.type == 'restaurant':
            arrival = later(time, travel_time)
            end_of_eating = later(arrival, eating_time)
            #check to see you arrive after it's open, end eating before its closed, and end eating before time is up
            if arrival > node.data.opening_time and end_of_eating < node.data.closing_time and end_of_eating < end_time:
                possible_edges.add((end_of_eating, node))

    return possible_edges

def movie_and_dinner_algo(graph, home_node, start_time, end_time, efficiency = 0, 
                                                                eating_time = 45):
    '''
    Takes the graph we had developed earlier and recursively traverses each node
    and all possibilities stemming from this node. When evaluating possible
    pathways, the algorithm first filters for legitmate possibilities. Then,
    for all nodes on these possible paths, evaluates the relative efficiency of
    the current path versus the most efficient path that has yet to reach this 
    node. For simplicity, we define efficiency as merely the sum of time up to
    the point in question of either watching a movie or eating food. If the 
    current pathway is more efficient than the previous, then we consider this
    node on the current path and set the efficiency of the node as the 
    current efficiency; elsewise, we drop it as a possibility. We store efficient
    pathways in a solution dictionary, which is returned. Ties are given to the 
    path that arrived at the point first, but certainly there could be more 
    complicated algorithms that use something like total travel time as a 
    tie-braker. Also, please note that there could also be additional ways to 
    define efficiency. We chose ours for its simplicity and appreciation of theatre_count
    outcome.
    '''
    sol_dict = {}

    possible_nodes = filter_data(start_time, end_time, home_node.edges)

    if possible_nodes == set([]):
        return sol_dict
    else:
        for possibility in possible_nodes:
            node = possibility[1]
            end_of_task = possibility[0]
            if node.data.type == 'movie': 
                efficiency += node.data.run_time
            elif node.data.type == 'restaurant':
                efficiency += eating_time
            if node.efficiency < efficiency:
                index = graph.index(node)
                graph[index] = node
                sol_dict[node] = movie_and_dinner_algo(graph, node, end_of_task, 
                                              end_time, efficiency, eating_time)

        return sol_dict

def get_solutions(sol_dict, output = []):
    '''
    Recurses through our solution dictionary and outputs a list of tuples, with
    each tuple possessing all the necessary data for output to the user.
    Basically, this function makes the data into as easy to comprehend form
    for the website as possible.
    '''
    if sol_dict == {}:
        #We use the string 'FLAG' to denote where one path stops
        output.append('FLAG')
    else:
        for node in sol_dict.keys():
            if node.data.type == 'movie':
                new_tup = (node.data.type, node.data.name, node.data.start, 
                           node.data.run_time, node.data.theatre,node.data.lat,
                           node.data.lng)
            if node.data.type == 'restaurant':
                new_tup = (node.data.type, node.data.name, node.data.price, 
                           node.data.rating, node.data.opening_time,
                           node.data.closing_time,node.data.lat, node.data.lng) 
            output.append(new_tup)
            get_solutions(sol_dict[node], output)

    return output

def go(restaurant_list, user_start, user_end, travel_mode, user_lat, user_lng,
         day_of_week):
    '''
    This function brings the entire file together, executing all the necessary
    functions in order to go from user input to user output
    '''
    
    home = Home(user_lat, user_lng)
    user_zip = get_zip(user_lat, user_lng)
    movie_data = get_all_movies(user_zip, day_of_week)
    movie_objs = get_movie_objs(movie_data, home, user_start, user_end, travel_mode)
    rest_objs = get_restaurant_objs(restaurant_list)
    (home_node, graph_of_travels) = get_graph(rest_objs, movie_objs, home, travel_mode)
    sol_dict = movie_and_dinner_algo(graph_of_travels, home_node, user_start, user_end)
    output = get_solutions(sol_dict)
    return output 
