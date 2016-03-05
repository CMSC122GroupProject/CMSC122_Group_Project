import bs4
import requests
import datetime
import sys
sys.path.insert(0, '/home/student/CMSC122_Group_Project/Gmaps')
import Maps

def get_url_flixster(zip_code):

    base_url = 'http://igoogle.flixster.com/igoogle/showtimes?movie=all&date='

    date = datetime.datetime.now()
    date_url = date.strftime("%Y%m%d")

    zip_url = '&postal='+str(zip_code)+'&submit=Go'

    url = base_url + date_url + zip_url

    return url

<<<<<<< HEAD
def get_movies_flixster(url):
=======
def clean_runtime(runtime):
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
    pm = 1200
    if start[-2:] == 'am':
        start = start[:-2]
        pm = 0
    start = start.split(":")
    if int(start[0]) == 12:
        pm = 0
    start = int(start[0] + start[1]) + pm
    return start

def get_movies(url):
>>>>>>> ce0d4041a88947c53d71ed366c3edec9651bcab3

    '''

    #Example usage of site
    Example_url = 'http://igoogle.flixster.com/igoogle/showtimes?movie=all&date=20160303&postal=21228&submit=Go'

    Ex_dict = {Theatre_name:{address:'', movies:{A:[time_1, time_2, time_3], B:[...]}}}
    '''

    data_dict = {}

    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.content, "html5lib")

    theatres = soup.find_all('div', class_ ='theater clearfix')

    for theatre in theatres:

        name = theatre.find('a').text

        data_dict[name] = {}

        address = theatre.find('h2').find('span').text
        
        left = address.index('-') + 1
        address = address[left:]

        right = address.index('-')

        address = address[:right].strip()

        data_dict[name]['address'] = address

        data_dict[name]['movies'] = {}

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


    return data_dict

def get_url_fandango(zip_code):
    '''
    Example_url = 'http://www.fandango.com/60615_movietimes?date=3/4/2016'
    '''

    base_url = 'http://www.fandango.com/'

    url_zip = base_url + str(zip_code)


    date = datetime.datetime.now()
    date_url = date.strftime("%m/%d/%Y")

    url = url_zip + '_movietimes?date=' + data

def update_movies_fandango(movie_dict):

    return

def movie_filter(movie_dict):

    return

class movie:
    def __init__(self, name, start, run_time, theatre, lat, lng):
        self.name = name
        self.start = start
        self.run_time = run_time
        self.theatre = theatre
        self.lat = lat  
        self.lng = lng

def get_movie_objs(data_dict):

    movies = set([])

    for theatre in data_dict.keys():
        address = data_dict[theatre]['address']
        (lat,lng) = Maps.get_coordinates(address)
        for name in data_dict[theatre]['movies'].keys():
            run_time = data_dict[theatre]['movies'][name]['run_time']
            for time in data_dict[theatre]['movies'][name]['start_times']:
                movie_obj = movie(name, time, run_time, theatre, lat, lng)
                movies.add(movie_obj)

    return movies

def movie_filter(data_objs, user_start, user_end, user_lat, user_lng):

    filtered_movies = set([])

    for movie in data_objs:
        if movie.start > user_start and  movie.start + movie.run_time < user_end:
            filtered_movies.add(movie)

    return filtered_movies

class Node:
    def __init__(self, label):
        self.label = label
        self.edges = []
    def add_edge(self, neighbor, weight):
        self.edges.append((neighbor, weight))

def dinner_and_movie(restuarants, movies, home):

    graph = set([])

    for movie in movies:
        
        for resturarant in restuarants:
            eat_and_watch.add((resturarant, movie))



    return
