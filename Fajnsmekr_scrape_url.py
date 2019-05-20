from lxml import html
from bs4 import BeautifulSoup
import requests
import csv
import re
import time

#VYTAHNE ZAKLADNI TABULKU VSECH RESTAURACI
url = "https://www.fajnsmekr.cz/"
search = "search_res.aspx?fulldata=brno"
res = requests.get(url + search)
soup = BeautifulSoup(res.text, "lxml")
table = soup.find("table", {"class": "mytxt"}) #tabulka s restauracemi
rows_name = table.findChildren("a")

#SEZNAM PRO ODKAZY NA RESTAURACE
links = []
for link in table.find_all('a', attrs={'href': re.compile("^restaurace.+\.aspx$")}): #najde odkazy restauraci
    links.append(link.get('href'))

#LOOP KTERY POSTUPNE PROJDE VSECHNY RESTAURACE
n = 0
for link in links:
    restaurant_url = requests.get(url + link, timeout=5)
    soup_restaurant = BeautifulSoup(restaurant_url.text, "lxml")
    description_rest = soup_restaurant.find("table",  {"class": "popisrest"})
    name_rest = rows_name[n].text


    date_reviews = []
    for review_date in soup_restaurant.find_all('td', text = re.compile('\d\d\.\d\d\.\d\d\d\d')): #vyhleda data a zapise do seznamu date_reviews
        date_review = review_date.text.strip()
        date_reviews.append(date_review)

    rest_reviews = soup_restaurant.find('table', {'class': 'mytxt'})
    reviews_to_file = [] #seznam pro zápis textu reviews do souboru
    no_rating = str(soup_restaurant.find('td', {'colspan': '7'}).text).strip()

    if no_rating == "Nehodnoceno":
        reviews_to_file.append("Nehodnoceno")
    else:
        byte_string = restaurant_url.content
        source_code = html.fromstring(byte_string)
        path = '//td/a/font[@class="zobrazhodn"][1]'
        tree = source_code.xpath(path)
        i = 0
        for review in tree:
            review = name_rest + "#" + date_reviews[i] + "#" + review.text_content().strip()
            reviews_to_file.append(review) #seznam pro zápis do souboru
            delete_comments = [re.sub(r'[\n*]?Koment.*([\n*]?.*)*', '', review) for review in reviews_to_file] #najde vsechny komentare a smaze
            clean_reviews = [re.sub(r'\n+', '', review) for review in delete_comments]

            i += 1

              #zápis reviews do csv
        with open('reviews.csv', 'a',encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for value in clean_reviews:
                writer.writerow([value])

    n += 1
