#desired parameteres: 'name', 'categories', 'location', 'rating', 'price range', 'food key word', 
#possible relations to run query on: 'yelp', 'google maps'

#from the Django interface well probably receive the following inputs for the algorithm:
    #a list of tuples (characterstic, metric) characteristics ordered from highest to lowest preference
#on a list from one to ten let's say, people will rank restuarant characteristic categories they care about the most
#what i indend to do then is run a SQL query with ALL stated search parameters incorporated in the query; 
#if the query returns restuarant results-great we're done; if not, I remove the least important search parameter from the querey and start again
#to make the SQL query doable-price range

#to reference the google maps api, probably going to be in real time as application is running

#sample dicitonaries to call on
#name, lon, lat, price-index, closing/opening time

#dict_api = {'yelp': ['name_id', 'price_lower', 'location_id', 'open_time', 'closing_time', 'food_spec'], 'maps' : ['distance', 'radius', 'location_id'], 
            #'twitter' : ['num_tweets', 'name_id']}
#from haversine import haversine
import sqlite3
import os
import re
#from Yelp import restaurants.db
#DATA_DIR = os.path.dirname(__file__)
#DATABASE_FILENAME = os.path.join(DATA_DIR, 'Yelp/restaurants.db')
DATABASE_FILENAME = '/home/student/cs122-win-16-asudit/CMSC122_Group_Project/asterisk_site/restaurants.db'


dict_api = {'yelp' : ['name_id', 'price', 'rating'], 'time' : ['m_open', 'm_closed', 't_open', 't_closed', 'w_open', 'w_closed', 'r_open', 'r_closed', 'f_open',
            'f_closed', 'sat_open', 'sat_closed', 'sun_open', 'sun_closed', 'name_id'], 'maps' : ['lon', 'lat', 'name_id']}

#not all of the attributes in our sample input would be included in output-some will be in the where statment etc
desired_output = ['name_id', 'price', 'rating']
ORDER_BY = 'ORDER BY yelp.name_id, yelp.price, yelp.rating' 

#some tables more important than others-eg yelp table more important than twitter etc
tables = ['yelp', 'time', 'maps']

#paramters for where statment in SQL query
dict_what = {'price' : ['yelp.price' + '<=' + '?']}
dict_what['distance'] = ['maps.distance' + '<=' + '?']
dict_what['rating'] = ['yelp.rating' + '>=' + '?']
dict_what['m_open'] = ['time.m_open' + '>=' + '?']
dict_what['m_closed'] = ['time.m_closed' + '<=' + '?']
dict_what['t_open'] = ['time.m_open' + '>=' + '?']
dict_what['t_closed'] = ['time.t_closed' + '<=' + '?']
dict_what['w_open'] = ['time.w_open' + '>=' + '?']
dict_what['w_closed'] = ['time.w_closed' + '<=' + '?']
dict_what['r_open'] = ['time.r_open' + '>=' + '?']
dict_what['r_closed'] = ['time.r_closed' + '<=' + '?']
dict_what['f_open'] = ['time.f_open' + '>=' + '?']
dict_what['f_closed'] = ['time.f_closed' + '<=' + '?']
dict_what['sat_open'] = ['time.sat_open' + '>=' + '?']
dict_what['sat_closed'] = ['time.sat_closed' + '<=' + '?']
dict_what['sun_open'] = ['time.sun_open' + '>=' + '?']
dict_what['sun_closed'] = ['time.sun_closed' + '<=' + '?']
#dict_what['name_id'] = ['yelp.name_id'  + '=' + '?']



#sample input (needs to be ordered):
sample = {'name_id':'KFC', 'price': 5, 'lon': 1.5, 'lat': 30, 'rating': 4 , 'm_open' : 800, 'm_closed' : 2100, 
'preferences' : ['name_id', 'distance', 'price', 'rating', 'm_open', 'm_closed' ] }

def query_relations(sample):
    relation_list = []
    relations = list(dict_api.keys())
    samples = list(sample.keys())
    for param in samples:
        for table in tables:
            if param in dict_api[table] and table in relation_list:
                break
            elif param in dict_api[table] and table not in relation_list:
                relation_list.append(table)

    return  relation_list

def query_join(sample):
    relation = query_relations(sample)
    join_on_list = []
    for table in relation:
        other = [i for i in relation if i != table]
        #print(other)
        for i in other:
            keys1 = set(dict_api[i])
            keys2 = set(dict_api[table])
            #print(keys1, keys2)
            key = list(keys1.intersection(keys2))
            #print(key)
            if key != []:
                    join1 = ".".join((table, key[0]))
                    join2 = ".".join((i, key[0]))
                    #print(join1, join2)
                    if table < i:
                        if ((join1, join2), (table, i)) not in join_on_list:
                            join_on_list.append(((join1, join2), (table, i)))
                    else:
                        if ((join2, join1), (i, table)) not in join_on_list:
                            join_on_list.append(((join2, join1), (i, table)))
    return join_on_list


def query_select(sample):
    
    relations = query_relations(sample)
    select_list = []
    count = []
    samples = list(sample.keys())
    print('sample:', samples)
    print('relations:', relations)
    #for param in sample:
    for param in desired_output:
        for table in relations:
            #if param in dict_api[table] and param in desired_output and param not in count:
            if param in dict_api[table] and param not in count:
                select_list.append(".".join((table, param)))
                count.append(param)
    return select_list


def query_where(sample):
    parameters = list(dict_what.keys())
    inputs = sample['preferences']
    what_list = []
    where_param = []
    for i in inputs:
        if i in parameters:
            if i == 'distance':
                pass
            else:
                what_list.append(dict_what[i])
                where_param.append(i)
    return what_list, where_param

def prelim_assembly(sample):
    SELECT = 'SELECT' + " "  + ",".join(query_select(sample))
    FROM = 'FROM' + " " + " JOIN ".join(query_relations(sample))
    on_list = []
    on_list_filter = []
    for i in query_join(sample):
        on_list.append(i[0])
    for i in on_list:
        on_list_filter.append("=".join(i))
    ON = "ON" + " " + " AND ".join(on_list_filter)
    where = []
    for i in query_where(sample)[0]:
        where = where + i
    WHERE = "WHERE" + " " + " AND ".join(where)
    query = SELECT + " " + FROM + " " + ON + " " + WHERE + " " + ORDER_BY
    quest_which = []
    for i in query_where(sample)[1]:
        quest_which.append(sample[i])
    return query, quest_which


def prelim_algorithm(sample):
    db = sqlite3.connect(DATABASE_FILENAME)
    c = db.cursor()
    s = prelim_assembly(sample)[0]
    args = prelim_assembly(sample)[1]
    #print(s, args)
    r = c.execute(s, args)
    result = r.fetchall()
    
    #db.close()
    return result

def algorithm(sample):
    query_return = prelim_algorithm(sample)
    #print('query return:', query_return)
    if len(sample['preferences']) == 0:
        #print('end reached')
        return []
    if query_return != []:
        #print('best case')
        return query_return
    else:
        least = sample['preferences'][-1]
        sample.pop(least, None)
        sample['preferences'].remove(least)
        #print('rework')
        return algorithm(sample)



    '''
    if query_return != []:
        return query_return
    else:
        least = sample['preferences'][-1]
        sample.pop(least, None)
        sample['preferences'].remove(least)
        prelim_algorithm(sample)
    #recursive strategy
   '''



    '''join_on_list.append(((join2, join1), (i, table)))
    check = []
    for i in join_on_list:
        check.append(i[1])
    for i in join_on_list:
        attribute = i[1][0]
        sketch = []
        other = [j  for j in join_on_list if j != i]
        for k in other:
            if attribute in k[1]:
                sketch.append(list(k[1])
        #sketch.remove(attribute)
        for test1 in sketch:
            for test2 in sketch:
                if test1 !=test2 and (test1,test2) in check:
                    join_on_list.remove((test1,test2))
    '''  
   
