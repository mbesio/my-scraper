from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20card'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

#Inspect the element - this should grab each product
containers = page_soup.findAll("div",{"class":"item-container"})

filename = "products.csv"
f = open(filename, "w")
headers = "brand, product_name\n"
f.write(headers)

#You cant then put the html in jsbeautiful to make it nice and readbale
for container in containers:
    brand = container.a.img["title"]
    title_container = container.findAll("div", {"class":"item-title"})

    f.write(brand + "," + "\n")
    f.close
