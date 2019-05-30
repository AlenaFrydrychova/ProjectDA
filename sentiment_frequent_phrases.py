import requests
import csv
import xlrd
import sys
import re
import heapq
import unicodedata
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

path_to_sentiment_xlsx = sys.argv[1]
#do příkazové řádky je třeba napsat příkaz ve formě -> nazev souboru + cesta
#Andy -> sentiment_frequent_phrases.py C:\\DA\\ProjectDA\\Excel\\sentiment.xlsx
#Alena -> sentiment_frequent_phrases.py C:\\Users\\Alena\\Documents\\DA_Czechitas\\projekt\\ProjectDA\\Excel\\sentiment.xlsx

#OTEVIRANI SOUBORU POMOCI KNIHOVNY XLRD, ROZDELENI OBSAHU PODLE RADKU
workbook = xlrd.open_workbook(path_to_sentiment_xlsx, 'rb')
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
    reviews.append(i[1])

'''
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



with open('reviews_analysis.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(zip(reviews, hodnoty_tofile, used_chars))
'''
#NAJDE 2 SLOVA PRED A ZA KLICOVYMI
def get_extracts(reviews, key_word):
    position = reviews_by_word.index(key_word)
    while position > 0:
        position = reviews_by_word.index(key_word, position+2)
        extracts_prev.append(reviews_by_word[position-2:position+1])
        extracts_next.append(reviews_by_word[position:position+2])
    return extracts_prev
    return extracts_next

reviews_string = ''.join(reviews)
reviews_string = reviews_string.lower()
reviews_by_word = reviews_string.split()
extracts_prev = []
extracts_next = []
key_words = ['jídlo', 'obsluha', 'restaurace']



for key_word in key_words:
    try:
        get_extracts(reviews, key_word)
    except ValueError:
        pass

#STOPWORDS WITH DIACRITICS LOWERCASE
prepositions = ["od","z","s","do","bez","krom","kromě","podle","okolo","vedle","během","prostřednictvím","u","za","k","před","na","oproti","naproti","proti","pro", "mimo", "pod","nad","mezi","skrz","o","po","v"]
conjunctions = ["že", "a", "i", "ani", "nebo", "či", "přímo", "nadto", "ani", "jak", "tak", "hned", "jednak", "zčásti", "dílem", "ale", "avšak", "však", "leč", "nýbrž", "naopak", "jenomže", "jenže", "sice", "jistě", "ale", "i", "ba", "ba i", "ba ani", "nadto", "dokonce", "nejen", "nebo", "anebo", "buď", "totiž", "vždyť", "neboť", "vždyť", "totiž", "však", "také", "proto", "a proto", "a tak", "tudíž", "a tudíž", "tedy"]
pronouns = ["já", "ty", "on", "ona", "ono", "my", "vy", "oni", "ony", "ona","se", "můj", "tvůj", "jeho", "její", "náš", "váš", "svůj", "ten", "tento", "tenhle", "onen", "takový", "týž", "tentýž", "sám", "kdo", "co", "jaký", "který","čí", "jenž", "nikdo", "nic", "nijaký", "ničí", "žádný", "někdo", "nějaký", "některý", "lecco", "něčí", "něco"]
#STOPWORDS WITHOUT DIACRITICS LOWERCASE
prepositions_without = [''.join((c for c in unicodedata.normalize('NFD', preposition) if unicodedata.category(c) != 'Mn')) for preposition in prepositions]
pronouns_without = [''.join((c for c in unicodedata.normalize('NFD', pronoun) if unicodedata.category(c) != 'Mn')) for pronoun in pronouns]
conjunctions_without = [''.join((c for c in unicodedata.normalize('NFD', conjunction) if unicodedata.category(c) != 'Mn')) for conjunction in conjunctions]
#STOPWORDS WITH DIACRITICS UPPERCASE
prepositions_upper = [preposition.upper() for preposition in prepositions]
conjuctions_upper = [conjuction.upper() for conjuction in conjunctions]
pronouns_upper = [pronoun.upper() for pronoun in pronouns]
#STOPWORDS WITHOUT DIACRITICS UPPERCASE
prepositions_upper_without = [preposition.upper() for preposition in prepositions_without]
conjuctions_upper_without = [conjuction.upper() for conjuction in conjunctions_without]
pronouns_upper_without = [pronoun.upper() for pronoun in pronouns_without]
stopwords_cz = prepositions + conjunctions + pronouns + prepositions_without + pronouns_without + conjunctions_without + prepositions_upper + conjuctions_upper + pronouns_upper + prepositions_upper_without + conjuctions_upper_without + pronouns_upper_without


extract_re = re.compile(r'^.*\.+.*$')
for extract in extracts_prev:
    for i in extract:
        if len(i) < 4:
            extract.remove(i)
        elif i.endswith('.') or i == extract_re or i in stopwords_cz:
            extract.remove(i)

for extract in extracts_next:
    for i in extract:
        if len(i) < 4:
            extract.remove(i)
        elif i.endswith('.') or i == extract_re or i in stopwords_cz:
            extract.remove(i)


#SKAREDY KOD PRO ROZDELENI UTRZKU PODLE TEMAT A ZJISTENI NEJCASTEJSICH SLOV
list_jidlo_prev = []
Dict_jidlo_prev = {}
list_jidlo_next = []
Dict_jidlo_next = {}

for extract in extracts_prev:
    if key_words[0] in extract:
        list_jidlo_prev.append(extract)

for extract in list_jidlo_prev:
    for word in extract:
        if word == 'jídlo':
            pass
        elif word in Dict_jidlo_prev:
            Dict_jidlo_prev[word] += 1
        else:
            Dict_jidlo_prev[word] = 1

Dict_jidlo_prev = heapq.nlargest(50, Dict_jidlo_prev, key=Dict_jidlo_prev.get)
#print(Dict_jidlo_prev)

for extract in extracts_next:
    if key_words[0] in extract:
        list_jidlo_next.append(extract)

for extract in list_jidlo_next:
    for word in extract:
        if word == 'jídlo':
            pass
        elif word in Dict_jidlo_next:
            Dict_jidlo_next[word] += 1
        else:
            Dict_jidlo_next[word] = 1

Dict_jidlo_next = heapq.nlargest(50, Dict_jidlo_next, key=Dict_jidlo_next.get)
#print(Dict_jidlo_next)


list_obsluha_prev = []
Dict_obsluha_prev = {}
list_obsluha_next = []
Dict_obsluha_next = {}

for extract in extracts_prev:
    if key_words[1] in extract:
        list_obsluha_prev.append(extract)

for extract in list_obsluha_prev:
    for word in extract:
        if word == 'obsluha':
            pass
        elif word in Dict_obsluha_prev:
            Dict_obsluha_prev[word] += 1
        else:
            Dict_obsluha_prev[word] = 1

Dict_obsluha_prev = heapq.nlargest(50, Dict_obsluha_prev, key=Dict_obsluha_prev.get)
#print(Dict_obsluha_prev)

for extract in extracts_next:
    if key_words[1] in extract:
        list_obsluha_next.append(extract)

for extract in list_obsluha_next:
    for word in extract:
        if word == 'obsluha':
            pass
        elif word in Dict_obsluha_next:
            Dict_obsluha_next[word] += 1
        else:
            Dict_obsluha_next[word] = 1

Dict_obsluha_next = heapq.nlargest(50, Dict_obsluha_next, key=Dict_obsluha_next.get)
#print(Dict_obsluha_next)


list_restaurace_prev = []
Dict_restaurace_prev = {}
list_restaurace_next = []
Dict_restaurace_next = {}

for extract in extracts_prev:
    if key_words[2] in extract:
        list_restaurace_prev.append(extract)


for extract in list_restaurace_prev:
    for word in extract:
        if word == 'restaurace':
            pass
        elif word in Dict_restaurace_prev:
            Dict_restaurace_prev[word] += 1
        else:
            Dict_restaurace_prev[word] = 1


for extract in extracts_next:
    if key_words[2] in extract:
        list_restaurace_next.append(extract)

for extract in list_restaurace_next:
    for word in extract:
        if word == 'restaurace':
            pass
        elif word in Dict_restaurace_next:
            Dict_restaurace_next[word] += 1
        else:
            Dict_restaurace_next[word] = 1

Dict_restaurace_prev = sorted(Dict_restaurace_prev.items(), key=lambda kv: kv[1], reverse=True)
Dict_restaurace_next = sorted(Dict_restaurace_next.items(), key=lambda kv: kv[1], reverse=True)

n = 0
for i in Dict_restaurace_prev:
    print(i, key_words[2], Dict_restaurace_next[n])
    n += 1


