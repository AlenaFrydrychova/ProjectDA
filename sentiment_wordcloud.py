import requests
import csv
import xlrd


"""
#FUKNCE NA ZJISTENI SENTIMENTU - POSLE REQUEST NA GENEEA.COM
def get_sentiment(chunk):
    payload = {
        'text': chunk,
        'user_key': 'b0273bf8e53597cc65ddaab58d6ad530',
        'domain': 'voc-hospitality'
    }
    r = requests.get('https://api.geneea.com/s2/sentiment', params=payload)
    return(r.json())
"""

#OTEVIRANI SOUBORU POMOCI KNIHOVNY XLRD, ROZDELENI OBSAHU PODLE RADKU
workbook = xlrd.open_workbook('C:\\Users\\Alena\\Documents\\DA Czechitas\\projekt\\ProjectDA\\Excel\\reviews.xlsx', 'rb')#('C:\\DA\\ProjectDA\\Excel\\reviews.xlsx', 'rb')
sheet = workbook.sheet_by_index(0)
rows = []
for i in range(sheet.nrows):
    columns = []
    for j in range(sheet.ncols):
        columns.append(sheet.cell(i, j).value)
    rows.append(columns)

# VYTAHNE Z RADKU 3. HODNOTU - REVIEW
reviews = []
for i in rows[1:]:
    reviews.append(i[2])

"""
#POUZIJE FUNKCI ANALYZUJ_RECENZI A HODNOTY ULOZI DO LISTU
hodnoty_tofile = []
for recenze in reviews:
        try:
            hodnoty_tofile.append(get_sentiment(recenze)['sentiment'])
        except KeyError:
            hodnoty_tofile.append('error')

#LIST PRO ZJISTENI MNOZSTVI POUZITYCH ZNAKU
used_chars = []
for element in reviews:
    used_chars.append(len(element))

"""

with open('\\csv\\reviews_analysis.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(zip(reviews, hodnoty_tofile, used_chars))

#NAJDE 2 SLOVA PRED A ZA KLICOVYMI
def get_extracts(reviews, key_word):
    position = reviews_by_word.index(key_word)
    while position > 0:
        position = reviews_by_word.index(key_word, position+2)
        extracts.append(reviews_by_word[position-2:position+3])
    return extracts

reviews_string = ''.join(reviews)
reviews_by_word = reviews_string.split()
extracts = []
key_words = ['jídlo', 'obsluha', 'restaurace']


for key_word in key_words:
    try:
        get_extracts(reviews, key_word)
    except ValueError:
        pass


extract_re = re.compile(r'^.*\.+.*$')
for extract in extracts:
    for i in extract:
        if len(i) < 4:
            extract.remove(i)
        elif i.endswith('.') or i == extract_re:
            extract.remove(i)


#SKAREDY KOD PRO ROZDELENI UTRZKU PODLE TEMAT A ZJISTENI NEJCASTEJSICH SLOV
list_jidlo = []
Dict_jidlo = {}

for extract in extracts:
    if key_words[0] in extract:
        list_jidlo.append(extract)

for extract in list_jidlo:
    for word in extract:
        if word in Dict_jidlo:
            Dict_jidlo[word] += 1
        else:
            Dict_jidlo[word] = 1

Dict_jidlo = heapq.nlargest(50, Dict_jidlo, key=Dict_jidlo.get)
print(Dict_jidlo)


list_obsluha = []
Dict_obsluha = {}

for extract in extracts:
    if key_words[1] in extract:
        list_obsluha.append(extract)

for extract in list_obsluha:
    for word in extract:
        if word in Dict_obsluha:
            Dict_obsluha[word] += 1
        else:
            Dict_obsluha[word] = 1

Dict_obsluha = heapq.nlargest(50, Dict_obsluha, key=Dict_obsluha.get)
print(Dict_obsluha)

list_restaurace = []
Dict_restaurace = {}

for extract in extracts:
    if key_words[2] in extract:
        list_restaurace.append(extract)

for extract in list_restaurace:
    for word in extract:
        if word in Dict_restaurace:
            Dict_restaurace[word] += 1
        else:
            Dict_restaurace[word] = 1

Dict_restaurace = heapq.nlargest(50, Dict_restaurace, key=Dict_restaurace.get)
print(Dict_restaurace)
