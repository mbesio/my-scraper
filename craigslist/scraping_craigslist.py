#link - https://towardsdatascience.com/web-scraping-craigslist-a-complete-tutorial-c41cea4f4981
#Download all of the Craigslisting listings in Oakland, with pics

from requests import get
from bs4 import BeautifulSoup as soup
import numpy as np
from time import sleep
import re
from random import randint #avoid throttling by not sending too many requests one after the other
from warnings import warn
from time import time
import pandas as pd



url = "https://sfbay.craigslist.org/search/sfc/apa?hasPic=1"

response = get(url)
page_soup = soup(response.text, "html.parser")

#get the html container of the housing posts
posts = page_soup.find_all('li', class_= 'result-row')

filename = "SF_housing.csv"
f = open(filename, "w", encoding='utf-8')
headers = "post_timing, neighborhood, post title, number bedrooms, sqft, URL, price\n"
f.write(headers)


#Build the loop on all the listings and on all the pages
results_num = page_soup.find('div', class_= 'search-legend')
results_total = int(results_num.find('span', class_='totalcount').text)
pages = np.arange(0, results_total+1, 120)

iterations = 0

post_timing = []
post_hoods = []
post_title_texts = []
bedroom_counts = []
sqfts = []
post_links = []
post_prices = []

for page in pages:

    #get requests
    response = get("https://sfbay.craigslist.org/search/sfc/apt?"
                   + "s=" #the parameter for defining the page number
                   + str(page) #the page number in the pages array from earlier
                   + "&hasPic=1"
                   + "&availabilityMode=0")


    sleep(randint(1,5))

    #throw warning for status codes that are not 200
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    #define the html text
    page_html = soup(response.text, 'html.parser')

    #define the posts
    posts = page_html.find_all('li', class_= 'result-row')

    for post in posts:
        if post.find('span', class_ = 'result-hood') is not None:
            #posting date
            #grab the datetime element 0 for date and 1 for time
            post_datetime = post.find('time', class_= 'result-date')['datetime']
            post_timing.append(post_datetime)

            #neighborhoods
            post_hood = post.find('span', class_= 'result-hood').text
            post_hoods.append(post_hood)

            #title text
            post_title = post.find('a', class_='result-title hdrlnk')
            post_title_text = post_title.text
            post_title_texts.append(post_title_text)

            #post link
            post_link = post_title['href']
            post_links.append(post_link)

            #removes the \n whitespace from each side, removes the currency symbol, and turns it into an int
            post_price = int(post.a.text.strip().replace("$", ""))
            post_prices.append(post_price)

            if post.find('span', class_ = 'housing') is not None:

                #if the first element is accidentally square footage
                if 'ft2' in post.find('span', class_ = 'housing').text.split()[0]:

                    #make bedroom nan
                    bedroom_count = np.nan
                    bedroom_counts.append(bedroom_count)

                    #make sqft the first element
                    sqft = int(post.find('span', class_ = 'housing').text.split()[0][:-3])
                    sqfts.append(sqft)

                #if the length of the housing details element is more than 2
                elif len(post.find('span', class_ = 'housing').text.split()) > 2:

                    #therefore element 0 will be bedroom count
                    bedroom_count = post.find('span', class_ = 'housing').text.replace("br", "").split()[0]
                    bedroom_counts.append(bedroom_count)

                    #and sqft will be number 3, so set these here and append
                    sqft = int(post.find('span', class_ = 'housing').text.split()[2][:-3])
                    sqfts.append(sqft)

                #if there is num bedrooms but no sqft
                elif len(post.find('span', class_ = 'housing').text.split()) == 2:

                    #therefore element 0 will be bedroom count
                    bedroom_count = post.find('span', class_ = 'housing').text.replace("br", "").split()[0]
                    bedroom_counts.append(bedroom_count)

                    #and sqft will be number 3, so set these here and append
                    sqft = np.nan
                    sqfts.append(sqft)

                else:
                    bedroom_count = np.nan
                    bedroom_counts.append(bedroom_count)

                    sqft = np.nan
                    sqfts.append(sqft)

                #if none of those conditions catch, make bedroom nan, this won't be needed
            else:
                bedroom_count = np.nan
                bedroom_counts.append(bedroom_count)

                sqft = np.nan
                sqfts.append(sqft)
                #    bedroom_counts.append(bedroom_count)

                #    sqft = np.nan
                #    sqfts.append(sqft)

        f.write(post_datetime.replace(","," ") + ',' + post_hood.replace(","," ") + ',' + post_title_text.replace(","," ") + ','+ str(bedroom_count)  + ',' + str(sqft) + ',' + post_link.replace(","," ") + ',' + '\n')
        #f.write(post_datetime + ',' + post_hood + ',' + post_title_text + ',' + bedroom_count + ',' + sqft + ',' + post_link + ',' + post_price + ',' + '\n')
        f.close

    iterations += 1
    print("Page " + str(iterations) + " scraped successfully!")

print("\n")
print("Scrape complete!")

import pandas as pd

eb_apts = pd.DataFrame({'posted': post_timing,
                       'neighborhood': post_hoods,
                       'post title': post_title_texts,
                       'number bedrooms': bedroom_counts,
                        'sqft': sqfts,
                        'URL': post_links,
                       'price': post_prices})
eb_apts.to_csv('exceltest.csv')
