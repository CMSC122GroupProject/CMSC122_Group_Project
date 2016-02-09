import json
import sqlite3

traffic = json.load(open('restuarant_data.json'))
db = sqlite3.connect("restaurants.sqlite")

c = db.cursor()

c.execute("CREATE TABLE food    \
         (timestamp text primary key,   \
          lon numeric,   \
          lat numeric,   \
          rating numeric, \
          review text)")

c.execute("DROP TABLE food")


db.close()

columns = ['long', 'lat', 'score', 'comments']
for key in traffic:
    data = traffic[key]
    keys = (key,) + tuple(data[c] for c in columns)
    print(str(keys))


'''
query = "INSERT INTO medicoes values (?,?,?,?,?,?,?)"
columns = ['local', 'coord', 'sentido', 'veiculos', 'modalidade', 'pistas']
for timestamp, data in traffic.iteritems():
    keys = (timestamp,) + tuple(data[c] for c in columns)
    c = db.cursor()
    c.execute(query, keys)
    c.close()


query = "CREATE TABLE "
'''