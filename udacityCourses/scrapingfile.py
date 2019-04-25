from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.udacity.com/courses/all'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div",{"class":"card-wrapper is-collapsed"})

#Create the csv file where I will scrape the information into

filename = "udacity_courses.csv"
f = open(filename, "w")
headers = "school, nano, level\n"
f.write(headers)

#Look on all the courses on the udacity page
for container in containers:
    school = container.h4.text
    nano = container.h3.text
    level =  container.find("div", {"class":"hidden-md-up level"}).text

    f.write(school + ',' + nano + ',' + level + ',' + '\n')
    f.close
