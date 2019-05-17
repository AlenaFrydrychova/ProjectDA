from lxml import html
from bs4 import BeautifulSoup
import requests
import csv
import re


url = "https://www.fajnsmekr.cz/"
search = "search_res.aspx?fulldata=brno"
res = requests.get(url + search, timeout=10)
soup = BeautifulSoup(res.text, "lxml")
table = soup.find("table", {"class": "mytxt"}) #tabulka s restauracemi
rows_name = table.findChildren("a")


links = []
for link in table.find_all('a', attrs={'href': re.compile("^restaurace.+\.aspx$")}): #najde odkazy restauraci
    links.append(link.get('href'))

n = 0
for link in links: 
    restaurant_url = requests.get(url + link, timeout=10)
    soup_restaurant = BeautifulSoup(restaurant_url.text, "lxml")
    description_rest = soup_restaurant.find("table",  {"class": "popisrest"})
    name_rest = rows_name[n].text

#najde tabulku s classou popisrest a v ní vyhledá všechny tabulky a dá je do řádků (nevim jestli to vysvětluju správně), 10 až 15 řádek je info o restauraci, které chceme
    output_rows = []
    for tag in description_rest.find_all('tr'): #celé informace o místě
        columns = tag.find_all('td')
        output_row = []
        for column in columns:
            output_row.append(column.text.strip())
        output_rows.append(output_row)

    date_reviews = []
    for review_date in soup_restaurant.find_all('td', text = re.compile('\d\d\.\d\d\.\d\d\d\d')):
        date_review = review_date.text.strip()
        date_reviews.append(date_review)
    #Reviews text -> Issue s komentáři komentářů !
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
            delete_comments = [re.sub(r'\n+Koment.+$', '', review) for review in reviews_to_file]
            clean_reviews = [re.sub(r'\n+', '', review) for review in delete_comments]
            print(clean_reviews)
            i += 1
    n += 1


    #zápis reviews do csv, pořád zapisuje i komentáře komentářů :(
with open('reviews.csv', 'w',encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for value in clean_reviews:
        writer.writerow([value])

    
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
#datum u reviews
    
