import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://www.fajnsmekr.cz/"
search = "search_res.aspx?fulldata=brno"
res = requests.get(url + search)
soup = BeautifulSoup(res.text, "lxml")
table = soup.find("table", {"class": "mytxt"}) #tabulka s restauracemi
rows_name = table.findChildren("a")
name_rest = rows_name[0].text #zatím jen název první restaurace

#for row in rows: #sem potom bdue muset přijít všechno co se bdue dít na další otevřené stránce

#celkové hodnocení restaurací, vynechává nuly, což je trochu problém
rest_rating = []
poradi = 1 #pocita poradi radku, ale vynechava radky, ktere neobsahuji "td", {"class": "hbg1"}

value_rating = 0
for line in table.find_all("td", {"class": "hbg1"}): #hledá v tabulce tagy td s classou hbg1 (tam je definovaná délka obrázku, který představuje hodnocení)
    if line != 0: #nefunguje, ideálně by se mělo spustit jen když v line tag td opravdu je a vypsat nulu, když není. Je třeba posunout podmínku nad cyklus a nějak jí přeformulovat?
        for rating in line.find_all("img"): #najde všechny tagy img v td s classou hbg1
            width = int(rating.get('width')) #hodnota width
            if width == 11: # 11 je maximální délka jedné kostičky hodnocení (za předpokladu, že není na konci -> ta má z nějakého důvodu 12)
                value_rating += width #hodnota do které se počítá rating jedné restaurace (celkový width obrázků)
                if width == 12: #pokud má 12 jedná se o poslední kosticku hodnoceni
                    value_rating += width #hodnota width
                    print(poradi, value_rating) #poradí je jen císlo řádku, když jsme to hledaly v tabulce na webu
                    value_rating = 0 #vymazání value rating, protože 12 má jen poslední kostička
                    poradi += 1
            elif width > 0 and width < 11: # kostička, která je na konci a není kompletní tzn je mezi 1 až 10
                value_rating += width #hodnota width
                print(poradi, value_rating)
                value_rating = 0 #vymazani hodnoty
                poradi += 1
    else: #nefunguje
        value_rating = 0
        print(value_rating)


 #poté bude v cyklu aby se název restaurace měnil
"""
url_rest = "restaurace/al_capone_pub.aspx"
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
"""
"""
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
"""
#Reviews text -> Issue s komentáři komentářů !
rest_reviews = soup_restaurant.find('table', {'class': 'mytxt'})
reviews_to_file = [] #seznam pro zápis textu reviews do souboru
no_rating = str(soup_restaurant.find('td', {'colspan': '7'}).text).strip()
print(no_rating)
if no_rating == "Nehodnoceno":
    reviews_to_file.append("Nehodnoceno")
    print(reviews_to_file)
else:
    for review in rest_reviews.find_all('font', {'class': 'zobrazhodn'}):# Filtruje jen texty! :D
        to_remove = review.find_all("div") #odstranila jsem tím komentář komentářů, ale nějakým záhadným způsobem tam je ještě jednou, přitom v html ho vidím jen jednou :D Div protože je to jediný div v tagu font
        for element in to_remove:
            element.extract()
        text_reviews = name_rest + "#" + review.text #zatím přidává jméno první restaurace, prootže nescrapujem všecky
        reviews_to_file.append(text_reviews) #seznam pro zápis do souboru

#zápis reviews do csv, pořád zapisuje i komentáře komentářů :(
with open('reviews.csv', 'w',encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for value in reviews_to_file:
        writer.writerow([value])
"""
