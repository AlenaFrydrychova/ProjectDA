import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://www.fajnsmekr.cz/"
search = "search_res.aspx?fulldata=brno"

res = requests.get(url + search)
soup = BeautifulSoup(res.text, "lxml")
table = soup.find("table", {"class": "mytxt"})
rows = table.findChildren("a")
#for row in rows: #sem potom bdue muset přijít všechno co se bdue dít na další otevřené stránce
#    print(url + row['href'])
name_rest = rows[0].text #poté bude v cyklu aby se název restaurace měnil
url_rest = "restaurace/cihelna1.aspx"
res1 = requests.get(url + url_rest)
soup_restaurant = BeautifulSoup(res1.text, "lxml")

#najde tabulku s classou popisrest a v ní vyhledá všechny tabulky a dá je do řádků (nevim jestli to vysvětluju správně), 10 až 15 řádek je info o restauraci, které chceme
description_rest = soup_restaurant.find("table",  {"class": "popisrest"})
output_rows = []
for tag in description_rest.find_all('tr'): #celé informace o místě
    columns = tag.find_all('td')
    output_row = []
    for column in columns:
        output_row.append(column.text.strip())
    output_rows.append(output_row)

#Adresa restaurace
rest_adress = output_rows[3][0].split("-")
street = re.split("(\d\d\d\d\d .+)",rest_adress[0])
postal_code_city = street_city[1].split(" ")

#Restaurace info -> zapisuje do csv, tady je asi vše ok
values_header = []
values_info = [name_rest, street[0], postal_code_city[1], postal_code_city[0]]
for row in output_rows[10:15]: # 10:15 protože v tomto intervalu jsou listy s informacemi, které chceme (vyzkoušela jsem na několika restauracích, vždy to je stejné(asi šablona))
    values_header.append(row[0]) #header pro hodnoty (stačí mít u jednoho)
    values_info.append(row[1]) #do souboru to chci tak abych zapisovala jen hodnoty parametrů (má/nemá parkoviště)
with open("info_rest.csv","w",encoding="utf-8",newline='') as csvfile:
    writer = csv.writer(csvfile)
    clean_header = ["Název restaurace", "Ulice", "Město", "PSČ"] #seznam pro očištění header values od dvojtečky
    for header in values_header:
        clean_header.append(header.replace(":","")) #header values bez dvojtečky
    writer.writerow(clean_header)#zapsání header do csv, při zapisování všech restaurací b mělo být asi mimo celkový cyklus
    writer.writerow(values_info)#zapsaní hodnot informací o restauraci
"""
#Reviews text -> Issue s komentáři komentářů !
rest_reviews = soup_restaurant.find('table', {'class': 'mytxt'})
reviews_to_file = [] #seznam pro zápis textu reviews do souboru
for review in rest_reviews.find_all('font', {'class': 'zobrazhodn'}):# Filtruje jen texty! :D
    to_remove = review.find_all("div") #odstranila jsem tím komentář komentářů, ale nějakým záhadným způsobem tam je ještě jednou, přitom v html ho vidím jen jednou :D Div protože je to jediný div v tagu font
    for element in to_remove:
        element.extract()
    text_reviews = name_rest + "#" + review.text
    reviews_to_file.append(text_reviews) #seznam pro zápis do souboru

#zápis reviews do csv, pořád zapisuje i komentáře komentářů :(
with open('reviews.csv', 'w',encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for value in reviews_to_file:
        writer.writerow([value])
"""
