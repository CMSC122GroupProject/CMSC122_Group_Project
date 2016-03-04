import bs4
import requests
import datetime

def get_url(zip_code):

    base_url = 'http://igoogle.flixster.com/igoogle/showtimes?movie=all&date='

    date = datetime.datetime.now()
    date_url = date.strftime("%Y%m%d")

    zip_url = '&postal='+str(zip_code)+'&submit=Go'

    url = base_url + date_url + zip_url

    return url

def get_movies(url):

    '''

    #Example usage of site
    Example_url = 'http://igoogle.flixster.com/igoogle/showtimes?movie=all&date=20160303&postal=21228&submit=Go'

    Ex_dict = {Theatre_name:{address:'', movies:{A:[time_1, time_2, time_3], B:[...]}}}
    '''

    data_dict = {}

    data = requests.get(url)
    soup = bs4.BeautifulSoup(data.content, "html5lib")

    theatres = soup.find_all('div', class_ ='theater clearfix')

    for theatre in theatres:

        name = theatre.find('a').text

        data_dict[name] = {}

        address = theatre.find('h2').find('span').text
        
        left = address.index('-') + 1
        address = address[left:]

        right = address.index('-')

        address = address[:right].strip()

        data_dict[name]['address'] = address

        data_dict[name]['movies'] = {}

        for movie in theatre.find('div', class_= 'showtimes clearfix').find_all('div', class_='showtime'):
            if movie.find('span'):            
                title = movie.find('h3').text.strip()
                
                try:
                    right = title.index('\n')
                except ValueError:
                    right = None
                title = title[:right]

                data_dict[name]['movies'][title] = {}

                run_time = movie.find('span').text
                left = run_time.rindex('-')
                run_time = run_time[left + 1:].strip()

                data_dict[name]['movies'][title]['run_time'] = run_time

                times = movie.text.strip() + '\xa0'

                left = times.index(':', times.index('\n'))
                right = times.rindex('\xa0')
                times = times[left -1 :right]

                times = times.replace(u'\xa0', u' ')
                times = times.replace('\n', '').replace('\t', '')
                
                data_dict[name]['movies'][title]['start_times'] = times.split(' ')

    return data_dict


