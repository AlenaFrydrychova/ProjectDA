import requests
from bs4 import BeautifulSoup
url = "https://www.fajnsmekr.cz/"
search = "search_res.aspx?fulldata=brno"

res = requests.get(url + search)
soup = BeautifulSoup(res.text, "lxml")
table = soup.find("table", {"class": "mytxt"})

rows = table.findChildren("a")
#for row in rows:
#    print(url + row['href'])
url_rest = "restaurace/tivoli_cafe.aspx"
res1 = requests.get(url + url_rest)
soup_restaurant = BeautifulSoup(res1.text, "lxml")



description_rest = soup_restaurant.find("table",  {"class": "popisrest"})

for tag in description_rest.find_all('td'):
    restaurant_info = tag.text



rest_reviews = soup_restaurant.find('table', {'class': 'mytxt'})

for tag in rest_reviews.find_all('td'):
    restaurant_reviews = tag.text
    print(restaurant_reviews)