#DOCUMENTAION~ORIGINAL (written mainly by Adam Sudit, with help from Ken Jung)


import sqlite3
import os
import re

#DATA_DIR = os.path.dirname(__file__)
#DATABASE_FILENAME = os.path.join(DATA_DIR, 'Yelp/restaurants.db')
DATABASE_FILENAME = '/home/student/cs122-win-16-asudit/CMSC122_Group_Project/asterisk_site/restaurants.db'
#DATABASE_FILENAME = '/home/student/CMSC122_Group_Project/asterisk_site/restaurants.db'


dict_api = {'yelp' : ['name_id', 'price', 'rating', 'comments'], 'time' : ['m_open', 'm_closed', 't_open', 't_closed', 'w_open', 'w_closed', 'r_open', 'r_closed', 'f_open',
            'f_closed', 'sat_open', 'sat_closed', 'sun_open', 'sun_closed', 'name_id'], 'maps' : ['lon', 'lat', 'name_id']}

#not all of the attributes in our sample input would be included in output-some will be in the where statment etc
desired_output = ['name_id', 'price', 'rating']

ORDER_BY = 'ORDER BY yelp.name_id, yelp.price, yelp.rating' 

#some tables more important than others-eg yelp table more important than twitter etc
tables = ['yelp', 'time', 'maps']


#paramters for where statment in SQL query
dict_what = {'price' : ['yelp.price' + '<=' + '?']}
dict_what['rating'] = ['yelp.rating' + '>=' + '?']
dict_what['m_open'] = ['time.m_open' + '<=' + '?']
dict_what['m_closed'] = ['? <= time.m_closed AND time.m_closed <= ?']
dict_what['t_open'] = ['time.t_open' + '<=' + '?']
dict_what['t_closed'] = ['? <= time.t_closed AND time.t_closed <= ?']
dict_what['w_open'] = ['time.w_open' + '<=' + '?']
dict_what['w_closed'] = ['? <= time.w_closed AND time.w_closed <= ?']
dict_what['r_open'] = ['time.r_open' + '<=' + '?']
dict_what['r_closed'] = ['? <= time.r_closed AND time.r_closed <= ?']
dict_what['f_open'] = ['time.f_open' + '<=' + '?']
dict_what['f_closed'] = ['? <= time.f_closed AND time.f_closed <= ?']
dict_what['sat_open'] = ['time.sat_open' + '<=' + '?']
dict_what['sat_closed'] = ['? <= time.sat_closed AND time.sat_closed <= ?']
dict_what['sun_open'] = ['time.sun_open' + '<=' + '?']
dict_what['sun_closed'] = ['? <= time.sun_closed AND time.m_closed <= ?']
dict_what['comments'] = ['yelp.comments REGEXP ?']

#sample input that algorithm takes ins
sample = { 'price': 5, 'lon': 1.5, 'lat': 30, 'rating': 4 , 'm_open' : 800, 'm_closed' : 2100, 'comments' : 'asdfads good'}

sample1 = { 'lon': -87.5966772, 'price': 1, 'lat': 41.8000353, 'rating': 2, 'm_open': 600, 'm_closed': 2400}

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

def remaker(words):
    words = words.split()
    words = ['(' + word + ')' for word in words ]
    rx = '|'.join(words)
    return rx

def query_relations(sample):
    '''
    given the search parameters, this function will indicate what tables
    will be needed for the SQL query
    '''
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
    '''
    returns a list of keys that are used to join one table to another, along 
    with said tables
    '''
    relation = query_relations(sample)
    join_on_list = []
    for table in relation:
        other = [i for i in relation if i != table]
        
        for i in other:
            keys1 = set(dict_api[i])
            keys2 = set(dict_api[table])
            key = list(keys1.intersection(keys2))
            if key != []:
                    join1 = ".".join((table, key[0]))
                    join2 = ".".join((i, key[0]))
                    if table < i:
                        if ((join1, join2), (table, i)) not in join_on_list:
                            join_on_list.append(((join1, join2), (table, i)))
                    else:
                        if ((join2, join1), (i, table)) not in join_on_list:
                            join_on_list.append(((join2, join1), (i, table)))
    return join_on_list


def query_select(sample):
    '''
    retuns the fields (referenced with respect to their table e.g yelp.name_id)
    desired for output
    '''
    relations = query_relations(sample)
    select_list = []
    count = []
    samples = list(sample.keys())
    for param in desired_output:
        for table in relations:
            if param in dict_api[table] and param not in count:
                select_list.append(".".join((table, param)))
                count.append(param)
    return select_list


def query_where(sample):
    '''
    this function will return two lists: one containing the actual parts of
    the SQL WHERE statement, to be joined by AND
    the other lists contains the list of attributes represented in the join
    '''
    parameters = list(dict_what.keys())
    inputs = list(sample.keys())
    what_list = []
    where_param = []
    for i in inputs:
        if i in parameters:
            if i[-6:] == 'closed':
                day = i[0]
                what_list.append(dict_what[i])
                where_param.append("_".join((day, 'open')))
                print("_".join((day, 'open')))
                where_param.append(i)
            else:
                what_list.append(dict_what[i])
                where_param.append(i)
            
    return what_list, where_param

def prelim_assembly(sample):
    '''
    Calls upon the previous helper functions to generate a SQL query string
    the second list are the parameter values of the ?'s in the SQL string WHERE statement
    '''

    SELECT = 'SELECT' + ' DISTINCT ' + ",".join(query_select(sample))

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
    query = SELECT + " " + FROM + " " + ON + " " + WHERE + " " + ORDER_BY + ' LIMIT 5'
    quest_which = []
    for i in query_where(sample)[1]:
        quest_which.append(sample[i])
    return query, quest_which


def prelim_algorithm(sample):
    '''
    this puts everything together: given the output of the previous 
    assembler we connect to SQL database and return the results of the query
    '''
    db = sqlite3.connect(DATABASE_FILENAME)
    db.create_function("REGEXP", 2, regexp)
    c = db.cursor()
    s = prelim_assembly(sample)[0]
    args = prelim_assembly(sample)[1]
    r = c.execute(s, args)
    result = r.fetchall()
    
    return result

def algorithm(sample):
    '''
    for novelty we kept this script: we orginally were going to 
    iterate the query if at first there were no outputs by eliminating search parameteres
    in succession arbitrarily. Later we decided against this approach
    '''
    if 'comments' in list(sample.keys()):
        sample['comments'] = remaker(sample['comments'])
    query_return = prelim_algorithm(sample)
    if len(sample['preferences']) == 0:
        return []
    if query_return != []:
        return query_return
    else:
        least = sample['preferences'][-1]
        sample.pop(least, None)
        sample['preferences'].remove(least)
        return algorithm(sample)

   
