# sql_maker.py - Original Code
# Author: Ken Jung
# Description: Puts the contents of the restaurants json dictionary and puts them
# into a sql database, implementing nltk in the process

import json
import sqlite3
from nltk.corpus import wordnet as wn

def trunk(num):
    '''
    Truncate numbers to two decimal places
    '''
    num = str(num)
    num = num.split('.')
    if len(num) < 2:
        return int(num[0])
    if len(num[1]) >= 2:
        return float(num[0] + '.' + num[1][:2])
    elif len(num[1]) == 1:
        return float(num[0] + '.' + num[1][0] + '0')

def format_time(time):
    '''
    Convert times to conform to military 24hr time
    '''
    if time == "Closed":
        return 0
    num = time[:-3]
    ap = time[-2:]
    time_parts = num.split(":")
    new_time = int(time_parts[0]) * 100 + int(time_parts[1])
    if ap == 'am' and int(time_parts[0]) != 12 or int(time_parts[0]) == 12 and ap == 'pm':
        return new_time
    return new_time + 1200

def insert_commands(restaurants):
    '''
    Construct the arguments to the sql INSERT commands
    '''
    args_yelp = []
    args_time = []
    args_maps = []
    for r in restaurants:
        data = restaurants[r]
        hours = data['hours']
        comments = data['comments']
        cm = set([])
        for word in comments:
            ss = wn.synsets(word, pos = 's') + wn.synsets(word, pos = 'r')
            if len(ss) > 0:
                lemmas = []
                for s in ss:
                    lemmas += s.lemmas() + s.lemmas()
                cm.update(lemmas)
        cm = list(cm)
        cm = [syn.name().split(".")[-1] for syn in cm]
        cm = " ".join(cm)
        time_to_append = []
        opening = [hours['Mon']['open'], hours['Tue']['open'], hours['Wed']['open'], hours['Thu']['open'], hours['Fri']['open'], hours['Sat']['open'], hours['Sun']['open']]
        closing = [hours['Mon']['close'], hours['Tue']['close'], hours['Wed']['close'], hours['Thu']['close'], hours['Fri']['close'], hours['Sat']['close'], hours['Sun']['close']]
        for i in range(7):
            time_to_append.append(format_time(opening[i]))
            time_to_append.append(format_time(closing[i]))
        time_to_append.append(data['name'])
        time_to_append.append(r)
        args_time.append(time_to_append)
        maps_to_append = [data['long'],  data['lat'], data['name'], r]
        yelp_to_append = [data['name'], len(data['price_index']), trunk(data['score']), cm, r]
        args_maps.append(maps_to_append)
        args_yelp.append(yelp_to_append)
    return (args_maps, args_yelp, args_time)

def go(read_in, write_to):
    '''
    Make the table. read_in is the filename of the json file, and write_to is
    the database to be written to (e.g. 'restaurants.db')
    '''
    restaurants = json.load(open(read_in))
    db = sqlite3.connect(write_to)
    c = db.cursor()
    time = "CREATE TABLE time (m_open int, m_closed int, t_open int, t_closed int, "
    time += "w_open int, w_closed int, r_open int, r_closed int, f_open int, f_closed int, "
    time += "sat_open int, sat_closed int, sun_open int, sun_closed int, name_id varchar(30), id varchar);"
    yelp = "CREATE TABLE yelp (name_id varchar(30), price int, rating float, comments varchar, id varchar);"
    maps = "CREATE TABLE maps (lon float, lat float, name_id varchar(30), id varchar);"
    timelist = "(m_open, m_closed, t_open, t_closed , w_open, w_closed, r_open, r_closed, f_open, f_closed, \
        sat_open, sat_closed, sun_open, sun_closed, name_id, id)"
    c.execute(time)
    c.execute(yelp)
    c.execute(maps)
    args_maps, args_yelp, args_time = insert_commands(restaurants)
    n = len(args_yelp)
    for i in range(n):
        args_yelp[i] = tuple(args_yelp[i])
        args_time[i] = tuple(args_time[i])
        args_maps[i] = tuple(args_maps[i])
    for i in range(n):
        c.execute("INSERT INTO yelp (name_id, price, rating, comments, id)  VALUES (?, ?, ?, ?, ?);", args_yelp[i])
        c.execute("INSERT INTO time" + timelist + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", args_time[i])
        c.execute("INSERT INTO maps VALUES (?, ?, ?, ?);", args_maps[i])

    db.commit()
    db.close()