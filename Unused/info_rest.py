import requests
from bs4 import BeautifulSoup
import csv
import re
import time
from geopy.geocoders import Nominatim
import sys
import xlrd
import pandas as pd

"""
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

#najde tabulku s classou popisrest a v ní vyhledá všechny tabulky a dá je do řádků (nevim jestli to vysvětluju správně), 10 až 15 řádek je info o restauraci, které chceme
n = 0
for link in links:
    output_rows = []
    restaurant_url = requests.get(url + link, timeout=5)
    soup_restaurant = BeautifulSoup(restaurant_url.text, "lxml")
    description_rest = soup_restaurant.find("table",  {"class": "popisrest"})
    name_rest = rows_name[n].text
    for tag in description_rest.find_all('tr'): #celé informace o místě
       columns = tag.find_all('td')
       output_row = []
       for column in columns:
           output_row.append(column.text.strip())
           output_rows.append(output_row)
    #Adresa restaurace
    rest_adress = output_rows[3][0].split("-")
    try:
        street_city = re.split("(6\d\d\d\d|\d\d\d \d\d)",rest_adress[0])
        postal_code = street_city[1].split(" ")
    except IndexError:
        street_city = rest_adress[0].split(" B")
        pass

    #Restaurace info -> zapisuje do csv, tady je asi vše ok
    values_info = [name_rest, street_city[0], postal_code[0], "Brno"]
    with open("info_rest.csv","a",encoding="utf-8",newline='') as csvfile:
       writer = csv.writer(csvfile)
       #clean_header = ["Název restaurace", "Ulice", "Město", "PSČ"] #seznam pro očištění header values od dvojtečky
       #writer.writerow(clean_header)#zapsání header do csv, při zapisování všech restaurací b mělo být asi mimo celkový cyklus
       writer.writerow(values_info)#zapsaní hodnot informací o restauraci
    n += 1

"""
#OTEVIRANI SOUBORU POMOCI KNIHOVNY XLRD, ROZDELENI OBSAHU PODLE RADKU
path_to_adresses_xlsx = sys.argv[1]
workbook = xlrd.open_workbook(path_to_adresses_xlsx, 'rb')
# C:\DA\ProjectDA\Excel\restaurant_adresses.xlsx
sheet = workbook.sheet_by_index(0)
rows = []
for i in range(sheet.nrows):
    columns = []
    for j in range(sheet.ncols):
        columns.append(sheet.cell(i, j).value)
    rows.append(columns)
name_of_rest = []
restaurant_adresses = []
for i in rows[1:]:
    name_of_rest.append(i[0])
    restaurant_adresses.append(i[4])


def get_adress(adresses):
    geolocator = Nominatim(user_agent="Czechitas/DA")
    location = geolocator.geocode(adresses)
    latitude = location.latitude
    longitude = location.longitude
    return latitude, longitude

i = 651
for adress in restaurant_adresses[651:]:
    with open("rest_adress.csv","a",encoding="utf-8",newline='') as csvfile:
       writer = csv.writer(csvfile)
       try:
           rest_location = get_adress(adress)
       except AttributeError:
           rest_location = "Neznámé"
       writer.writerow([name_of_rest[i]]+[rest_location])
    time.sleep(0.5)
    i += 1
