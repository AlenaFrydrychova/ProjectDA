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

reviews_to_file = [] #seznam pro zápis textu reviews do souboru
for review in rest_reviews.find_all('font', {'class': 'zobrazhodn'}):# Filtruje jen texty! :D
    text_reviews = review.text
    reviews_to_file.append(text_reviews) #seznam pro zápis do souboru
    print(text_reviews)

"""
for tag in rest_reviews.find_all('td'): #tady třeba nějak vyfiltrovat jednotlivé části -> tzn útrata, počet osob, počet hodnocení?, samotný text, autor
    restaurant_reviews = tag.text
    reviews_to_file.append(rest_reviews.text) #seznam pro zápis do souboru
bad_chars = ["\n","\t", "Zobraz všechny komentáře"] # nějak smazat mezery?

print(reviews_to_file)
"""

with open('reviews.csv', 'w', encoding='utf-8') as f:
    for item in reviews_to_file:
        f.write(item + "\n")
        
