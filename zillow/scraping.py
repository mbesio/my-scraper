from bs4 import BeautifulSoup
import requests

my_url = 'https://www.zillow.com/homes/for_sale/Oakland-CA/13072_rid/7_days/0-1200_size/globalrelevanceex_sort/37.943114,-121.970559,37.639791,-122.486916_rect/10_zm/0_mmm/'
my_url2 = 'https://www.zillow.com/homes/for_sale/Oakland-CA/13072_rid/7_days/0-1200_size/globalrelevanceex_sort/37.943385,-121.970558,37.640063,-122.486916_rect/10_zm/2_p/0_mmm/'

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

with requests.Session() as s:
    url = 'https://www.zillow.com/homes/for_sale/Oakland-CA/13072_rid/7_days/0-1200_size/globalrelevanceex_sort/37.943114,-121.970559,37.639791,-122.486916_rect/10_zm/0_mmm/'
    r = s.get(url, headers=req_headers)

soup = BeautifulSoup(r.content, 'lxml')

prices = soup.findAll("span", {"class":"zsg-photo-card-price"})
infos = soup.findAll('span', {'class': 'zsg-photo-card-info'})
addresses = soup.findAll('span', {'itemprop': 'address'})

filename = "listing.csv"
f = open(filename, "w")
headers = "price, info, address\n"
f.write(headers)

#for price, info, address in prices, infos, addresses:
#    prezzo = price.text
#    inform = info.text
#    indirizzo = address.text

#    f.write(prezzo + "," + inform + "," + indirizzo + "\n")
#    f.close

for price in prices:
    prezzo = price.text
    f.write(prezzo.replace(",","") + "\n")
    f.close
