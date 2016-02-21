import json
import sqlite3

restaurants = json.load(open('restuarant_data.json'))
db = sqlite3.connect("restaurants.db")

c = db.cursor()

time = "CREATE TABLE time (m_open int, m_closed int, t_open int, t_closed int, "
time += "w_open int, w_closed int, r_open int, r_closed int, f_open int, f_closed int, "
time += "sat_open int, sat_closed int, sun_open int, sun_closed int, name_id varchar(30));"
yelp = "CREATE TABLE yelp (name_id varchar(30), price int, rating float);"
maps = "CREATE TABLE maps (lon float, lat float, name_id varchar(30));"

timelist = "(m_open, m_closed, t_open, t_closed , w_open, w_closed, r_open, r_closed, f_open, f_closed, \
    sat_open, sat_closed, sun_open, sun_closed, name_id)"

c.execute(time)
c.execute(yelp)
c.execute(maps)

args_yelp = []
args_time = []
args_maps = []

def format_time(time):
    if time == "Closed":
        return 0
    num = time[:-3]
    ap = time[-2:]
    time_parts = num.split(":")
    new_time = int(time_parts[0] + time_parts[1])
    if ap == 'am':
        return new_time
    return new_time + 1200

for r in restaurants:
    data = restaurants[r]
    hours = data['hours']
    time_to_append = []
    opening = [hours['Mon']['open'], hours['Tue']['open'], hours['Wed']['open'], hours['Thu']['open'], hours['Fri']['open'], hours['Sat']['open'], hours['Sun']['open']]
    closing = [hours['Mon']['close'], hours['Tue']['close'], hours['Wed']['close'], hours['Thu']['close'], hours['Fri']['close'], hours['Sat']['close'], hours['Sun']['close']]
    for i in range(7):
        time_to_append.append(format_time(opening[i]))
        time_to_append.append(format_time(closing[i]))
    time_to_append.append(data['name'])
    args_time.append(time_to_append)
    maps_to_append = [data['long'],  data['lat'], data['name']]
    yelp_to_append = [data['name'], len(data['price_index']), data['score']]
    args_maps.append(maps_to_append)
    args_yelp.append(yelp_to_append)

n = len(args_yelp)
for i in range(n):
    args_yelp[i] = tuple(args_yelp[i])
    args_time[i] = tuple(args_time[i])
    args_maps[i] = tuple(args_maps[i])

for i in range(n):
    c.execute("INSERT INTO yelp (name_id, price, rating)  VALUES (?, ?, ?);", args_yelp[i])
    c.execute("INSERT INTO time" + timelist + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", args_time[i])
    c.execute("INSERT INTO maps VALUES (?, ?, ?);", args_maps[i])

db.commit()
db.close()