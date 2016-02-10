import json
import sqlite3

traffic = json.load(open('restuarant_data.json'))
db = sqlite3.connect("restaurants.sqlite")

c = db.cursor()

time = "CREATE TABLE time (m_open numeric, m_closed numeric, t_open numeric, t_closed numeric, "
time += "w_open numeric, w_closed numeric, r_open numeric, r_closed numeric, f_open numeric, f_closed numeric, "
time += "sat_open numeric, sat_closed numeric, sun_open numeric, sun_closed numeric, name_id text);"
yelp = "CREATE TABLE yelp (name_id text, price int, rating numeric);"
maps = "CREATE TABLE maps (lon numeric, lat numeric, name_id text);"

c.execute(time)
c.execute(yelp)
c.execute(maps)

db.close()


'''

columns = ['long', 'lat', 'score', 'comments']
for key in traffic:
    data = traffic[key]
    keys = (key,) + tuple(data[c] for c in columns)
    print(str(keys))
'''