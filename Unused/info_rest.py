#najde tabulku s classou popisrest a v ní vyhledá všechny tabulky a dá je do řádků (nevim jestli to vysvětluju správně), 10 až 15 řádek je info o restauraci, které chceme
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
