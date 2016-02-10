import sqlite3
import random

random.seed(10)
XMIN = 41.795283
XMAX = 41.802335
YMIN = -87.596666
YMAX = -87.584138

db = sqlite3.connect("restaurants.sqlite")

c = db.cursor()

c.execute("DROP TABLE time")
c.execute("DROP TABLE yelp")
c.execute("DROP TABLE maps")

time = "CREATE TABLE time (m_open, m_closed, t_open, t_closed, "
time += "w_open, w_closed, r_open, r_closed, f_open, f_closed, "
time += "sat_open, sat_closed, sun_open, sun_closed, name_id);"
yelp = "CREATE TABLE yelp (name_id, price, rating);"
maps = "CREATE TABLE maps (lon, lat, name_id);"

timelist = "(m_open, m_closed, t_open, t_closed , w_open, w_closed, r_open, r_closed, f_open, f_closed, \
    sat_open, sat_closed, sun_open, sun_closed, name_id)"

c.execute(time)
c.execute(yelp)
c.execute(maps)

restaurants = ['Valois', 'Snail Thai', 'Chipotle', 'Medici', 'Harolds Chicken Shack']
args_yelp = [['Valois', 2, 3.978], ['Snail Thai', 3, 4.294], ['Chipotle', 3, 4.422], \
                ['Medici', 3, 3.851], ['Harolds Chicken Shack', 1, 3.825]]
args_time = []
args_maps = []

for r in restaurants:
    time_to_append = []
    opening = [random.randint(6,10)*100 for i in range(7)]
    closing = [random.randint(19,24)*100 for i in range(7)]
    for i in range(7):
        time_to_append.append(opening[i])
        time_to_append.append(closing[i])
    time_to_append.append(r)
    maps_to_append = [random.uniform(XMIN, XMAX), random.uniform(YMIN, YMAX),r]
    args_time.append(time_to_append)
    args_maps.append(maps_to_append)

for i in range(5):
    args_yelp[i] = tuple(args_yelp[i])
    args_time[i] = tuple(args_time[i])
    args_maps[i] = tuple(args_maps[i])

print(args_yelp)
print(args_time)
print(args_maps)

for i in range(5):
    c.execute("INSERT INTO yelp (name_id, price, rating)  VALUES (?, ?, ?);", args_yelp[i])
    c.execute("INSERT INTO time" + timelist + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", args_time[i])
    c.execute("INSERT INTO maps VALUES (?, ?, ?);", args_maps[i])

db.close()

