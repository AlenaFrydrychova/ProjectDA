import requests
import csv
import xlrd
<<<<<<< HEAD

=======
import re
import heapq
import unicodedata
>>>>>>> 9b668bee3dde192491fc0afcba8b46b04bbb3d92

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



with open('\\csv\\reviews_analysis.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(zip(reviews, hodnoty_tofile, used_chars))


'''

#STOPWORDS WITH DIACRITICS LOWERCASE
prepositions = ["od","z","s","do","bez","krom","kromě","podle","okolo","vedle","během","prostřednictvím","u","za","k","před","na","oproti","naproti","proti","pro", "mimo", "pod","nad","mezi","skrz","o","po","v"]
conjunctions = ["a", "i", "ani", "nebo", "či", "přímo", "nadto", "ani", "jak", "tak", "hned", "jednak", "zčásti", "dílem", "ale", "avšak", "však", "leč", "nýbrž", "naopak", "jenomže", "jenže", "sice", "jistě", "ale", "i", "ba", "ba i", "ba ani", "nadto", "dokonce", "nejen", "nebo", "anebo", "buď", "totiž", "vždyť", "neboť", "vždyť", "totiž", "však", "také", "proto", "a proto", "a tak", "tudíž", "a tudíž", "tedy"]
pronouns = ["já", "ty", "on", "ona", "ono", "my", "vy", "oni", "ony", "ona","se", "můj", "tvůj", "jeho", "její", "náš", "váš", "svůj", "ten", "tento", "tenhle", "onen", "takový", "týž", "tentýž", "sám", "kdo", "co", "jaký", "který","čí", "jenž", "nikdo", "nic", "nijaký", "ničí", "žádný", "někdo", "nějaký", "některý", "lecco", "něčí", "něco"]
verbs = ["být","bejt","jsem","jsi","je","jest","jsme","jste","jsou","budu","budeš","bude","budeme","budete","budou","buď","budiž","buďme","buďmež","buďte","buďtež","byl","byla","bylo","byli","byly","jsa","jsouc","jsouce","byv","byvše","byvši","bych","bychom","bys","byste","by", "seš", "mám","máš","má","máme","máte","mají","měj","mějme","mějte","měl","měla","mělo","měli","měly","maje","majíc","majíce"]
another_specific = ["si","jen","mi","mě","tady","tomu","že","to","nám","ná","takže","jako","už","pokud","asi","celkem","docela","tam","dali","ze","ve","ji","ta","pak","taky","což","tím","již","možná","která","toho","protože","sem","kde","která","které","tu","než","když","Kč","při","až","ho","této","mne","aby","nebyl","tuto","tom","No","kdy","dal","nebyla","jejich","jinak","zde","kterou","toto","dala","ní","nás","mu","dostali","objednali","jím","myslím","jim"]

#STOPWORDS WITHOUT DIACRITICS LOWERCASE
prepositions_without = [''.join((c for c in unicodedata.normalize('NFD', preposition) if unicodedata.category(c) != 'Mn')) for preposition in prepositions]
pronouns_without = [''.join((c for c in unicodedata.normalize('NFD', pronoun) if unicodedata.category(c) != 'Mn')) for pronoun in pronouns]
conjunctions_without = [''.join((c for c in unicodedata.normalize('NFD', conjunction) if unicodedata.category(c) != 'Mn')) for conjunction in conjunctions]
verbs_without = [''.join((c for c in unicodedata.normalize('NFD', verb) if unicodedata.category(c) != 'Mn')) for verb in verbs]

#STOPWORDS WITH DIACRITICS UPPERCASE
prepositions_upper = [preposition.upper() for preposition in prepositions]
conjuctions_upper = [conjuction.upper() for conjuction in conjunctions]
pronouns_upper = [pronoun.upper() for pronoun in pronouns]
verbs_upper = [verb.upper() for verb in verbs]

#STOPWORDS WITHOUT DIACRITICS UPPERCASE
prepositions_upper_without = [preposition.upper() for preposition in prepositions_without]
conjuctions_upper_without = [conjuction.upper() for conjuction in conjunctions_without]
pronouns_upper_without = [pronoun.upper() for pronoun in pronouns_without]
verbs_upper_without = [verb.upper() for verb in verbs_without]

stopwords = prepositions + conjunctions + pronouns + verbs + prepositions_without + pronouns_without + conjunctions_without + verbs_without + prepositions_upper + conjuctions_upper + pronouns_upper + verbs_upper + prepositions_upper_without + conjuctions_upper_without + pronouns_upper_without + verbs_upper_without + another_specific



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

<<<<<<< HEAD
for key, value in DictOfWords.items():
    if value == max_value:
        print(key)
=======
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









'''
#WORDCLOUD
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

reviews = [review.strip() for review in reviews]
reviews_dict = {"review" : reviews} #z lsitu slovník, aby měl sloupec header (určitě jde i jinak)
df = pd.DataFrame(reviews_dict) #pandas dataframe ze slovníku reviews
text = " ".join(review for review in df.review) #recenze

wordcloud = WordCloud(width=800, height=400, stopwords=stopwords, max_words=120, background_color="white").generate(text)

plt.figure(figsize=(15,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

wordcloud.to_file("img\\all_reviews.png")
'''
>>>>>>> 9b668bee3dde192491fc0afcba8b46b04bbb3d92
