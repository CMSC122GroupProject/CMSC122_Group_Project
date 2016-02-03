#In case we can't get the API working, this would be a fine alternative

import bs4
import requests

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
        print(page_urls)
        new_restuarants = restuarant_hopper(soup, domain)
        restuarant_urls = restuarant_urls.union(new_restuarants)

    return restuarant_urls


