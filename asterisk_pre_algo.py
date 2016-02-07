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

dict_api = {'yelp': ['name_id', 'price_lower', 'location_id', 'open_time', 'closing_time', 'food_spec'], 'maps' : ['distance', 'radius', 'location_id'], 
            'twitter' : ['num_tweets', 'name_id']}

#not all of the attributes in our sample input would be included in output-some will be in the where statment etc
desired_output = ['name_id', 'location', 'distance']

#some tables more important than others-eg yelp table more important than twitter etc
tables = ['yelp', 'maps', 'twitter']

#paramters for where statment in SQL query
dict_what = {'price_lower' : ['yelp.price_lower' + '>=' + '?']}


#sample input:
sample = {'name_id':'Medici', 'price_lower' : 10, 'price_upper': 15, 'distance': 1.5, 'rating': 3.5, 'food_spec': ['sandwich', 'bakery', 'coffee']}

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
        for i in other:
            keys1 = set(dict_api[i])
            keys2 = set(dict_api[table])
            key = list(keys1.intersection(keys2))
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
    samples = list(sample.keys())
    for param in samples:
        for table in relations:
            if param in dict_api[table] and param in desired_output:
                select_list.append(".".join((table, param)))
    return select_list


def query_where(sample):



                
   
