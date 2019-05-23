import requests
import csv
import xlrd
#import unicodedata

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

print(extracts)


#IN PROGRESS
DictOfWords = {}

max_value = 0

for extract in extracts:
  if extract in DictOfWords:
    DictOfWords[extract] += 1
    if DictOfWords[extract] > max_value:
        max_value = DictOfWords[extract]

  else:
    DictOfWords[extract] = 1

for key, value in DictOfWords.items():
    if value == max_value:
        print(key)



"""
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
"""