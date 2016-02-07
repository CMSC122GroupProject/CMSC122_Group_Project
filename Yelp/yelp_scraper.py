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

    data_out = {}

    for url in url_list:
        data = requests.get(url)
        soup = bs4.BeautifulSoup(data.content, "html5lib")
        #coordinates
        coordinate = soup.find('div', class_='lightbox-map hidden')
        json_data = coordinate["data-map-state"]
        json_string = json_data.replace("'", "\"")
        d = json.loads(json_string)
        data_out['lat'] = d['center']['latitude']
        data_out['long'] = d['center']['longitude']
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
        data_out["score"] = exact_score
        #comments
        #right now only scrapes first page of comments but we can (and probably should) reimplement
        #it to take multiple
        data_out["comments"] = []
        for rating in soup.find_all("div", class_="review-content"):
            for description in rating.find_all("p", itemprop="description"):
                data_out["comments"].append(description.text)
        #recommended food?
    #save to json
    with open('restuarant_data.json', 'w') as fp:
        json.dump(data_out, fp)