#In case we can't get the API working, this would be a fine alternative

import bs4
import requests
import json

def page_hopper(soup, domain):

    page_urls = set([])
    
    for link in soup.find_all('a', class_="available-number pagination-links_anchor"):
        if link.get('href'):
            url = set([domain + link.get('href')])
            page_urls = page_urls.union(url)

    return page_urls

def restuarant_hopper(soup, domain):

    restuarant_urls = set([])

    for link in soup.find_all('a', class_="biz-name"):
        if link.get('href'):
            url = set([domain + link.get('href')])
            restuarant_urls = restuarant_urls.union(url)

    return restuarant_urls

def proof(starting_url, domain):

    page_urls = set([starting_url])
    restuarant_urls = set([])
    sites_visited = set([])
    
    #should probably remove the '?seach_key=...' portion of the url

    while page_urls != set([]):
        current_url = page_urls.pop()
        sites_visited = sites_visited.union(set([current_url]))
        data = requests.get(current_url)
        soup = bs4.BeautifulSoup(data.content, "html5lib")

        new_pages = page_hopper(soup, domain)
        page_urls = page_urls.union(new_pages.difference(sites_visited))

        new_restuarants = restuarant_hopper(soup, domain)
        restuarant_urls = restuarant_urls.union(new_restuarants)

    return restuarant_urls

def data_gather(url_list):
    #set of common english words, cleaned over informally
    skip_words = set(['the','be','and','of','a','in','to','have','to','it','I','that',
                      'for','you','he','with','on','do','say','this','they','at','but',
                      'we','his','from','that','not',"n't",'by','she','or','as','what',
                      'go','their','can','who','get','if','would','her','all','my','make',
                      'about','know','will','as','up','one','time','there','year','so','think',
                      'when','which','them','some','me','out','into','just','see','him','your',
                      'come','could','now','than','like','other','how','then','its','our',
                      'more','these','want','way','look','also','because','day','more','use',
                      'no','find','here','thing','give','many','well','only','those','tell',
                      'very','is', 'i', 'even','back','any','through','us'])

    data_out = {}

    for url in url_list:
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.content, "html5lib")
        #yelp_id/unique identifier
        yelp_id = soup.find("meta", {"name":"yelp-biz-id"})["content"]
        data_out[yelp_id] = {}
        #biz name
        data_out[yelp_id]["name"] = soup.find("h1", class_="biz-page-title embossed-text-white shortenough").text.strip()
        #coordinates
        coordinate = soup.find('div', class_='lightbox-map hidden')
        json_data = coordinate["data-map-state"]
        json_string = json_data.replace("'", "\"")
        d = json.loads(json_string)
        data_out[yelp_id]['lat'] = d['center']['latitude']
        data_out[yelp_id]['long'] = d['center']['longitude']
        #exact score
        scores = soup.find('table', class_="histogram histogram--alternating histogram--large")
        stars = 5
        score_count = 0
        votes_count = 0
        for score in scores.find_all("td", class_="histogram_count"):
            num_votes = float(score.text)
            votes_count = votes_count + num_votes
            score_count = score_count +  num_votes * stars
            stars = stars - 1
        exact_score = score_count / votes_count
        data_out[yelp_id]["score"] = exact_score
        #comments
        #right now only scrapes first page of comments but we can (and probably should) reimplement
        #it to take multiple
        data_out[yelp_id]["comments"] = []
        for rating in soup.find_all("div", class_="review-content"):
            for description in rating.find_all("p", itemprop="description"):
                words = description.text.lower().split()
                for word in words:
                    if not word in skip_words:
                        data_out[yelp_id]["comments"].append(word)
        #hours
        #price range
        data_out[yelp_id]["price_range"] = soup.find('dd', class_="nowrap price-description").text.strip()
        #price index
        #should be able to do a simple length function if we want
        data_out[yelp_id]["price_index"] = soup.find("span", class_="business-attribute price-range").text
        #schedule
        data_out[yelp_id]["hours"] = {}
        hours_table = soup.find("table", class_="table table-simple hours-table")
        rows = hours_table.find_all("tr")
        for day in rows:
            date = day.find("th")
            day_of_week = date.text
            data_out[yelp_id]["hours"][day_of_week] = {}
            hours = day.find("td").find_all("span", class_="nowrap")
            if hours == []:
                data_out[yelp_id]["hours"][day_of_week]["open"] = "Closed"
                data_out[yelp_id]["hours"][day_of_week]["close"] = "Closed"
            else:   
                open_time = hours[0].text
                close_time = hours[1].text
                data_out[yelp_id]["hours"][day_of_week]["open"] = open_time
                data_out[yelp_id]["hours"][day_of_week]["close"] = close_time
        #type of resturant
        restuarant_type = soup.find("span", class_="category-str-list").text.splitlines() #might need to include this strip method elsewhere
        data_out[yelp_id]["rest_types"] = []
        for types in restuarant_type:
            desc = types.strip()
            if desc != "":
                data_out[yelp_id]["rest_types"].append(desc)
        #extra info
        for attribute in soup.find("div", class_="short-def-list").find_all("dl"):
            data_out[yelp_id][attribute.find("dt", class_="attribute-key").text.strip()] = attribute.find("dd").text.strip()

    #save to json
    with open('restuarant_data.json', 'w') as fp:
        json.dump(data_out, fp)