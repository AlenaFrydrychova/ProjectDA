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
#Andy -> sentiment_frequent_phrases.py C:\DA\ProjectDA\Excel\sentiment.xlsx
#Alena -> sentiment_frequent_phrases.py C:\Users\Alena\Documents\DA_Czechitas\projekt\ProjectDA\Excel\sentiment.xlsx

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
conjunctions = ["protože", "když", "jako", "takže", "že", "a", "i", "ani", "nebo", "či", "přímo", "nadto", "ani", "jak", "tak", "hned", "jednak", "zčásti", "dílem", "ale", "avšak", "však", "leč", "nýbrž", "naopak", "jenomže", "jenže", "sice", "jistě", "ale", "i", "ba", "ba i", "ba ani", "nadto", "dokonce", "nejen", "nebo", "anebo", "buď", "totiž", "vždyť", "neboť", "vždyť", "totiž", "však", "také", "proto", "a proto", "a tak", "tudíž", "a tudíž", "tedy"]
pronouns = ["mé", "toto", "tím", "by", "ta", "já", "ty", "on", "ona", "ono", "my", "vy", "oni", "ony", "ona","se", "můj", "tvůj", "jeho", "její", "náš", "váš", "svůj", "ten", "tento", "této", "tato", "tahle", "téhle", "to", "se", "tenhle", "onen", "takový", "týž", "tentýž", "sám", "kdo", "co", "jaký", "který","čí", "jenž", "nikdo", "nic", "nijaký", "ničí", "žádný", "někdo", "nějaký", "některý", "lecco", "něčí", "něco"]
others = ['tomu', '(ale', 'taky', 'aby', 'abych', 'pak', 'všem', 'bych', 'jiná', 'mnou', 'přes', 'jiné', 'si', 'naši', 'naší', 'vaši', 'vaší', 'prostě', 'tomto', 'mně', 'např', 'např.', ',', 'tak', 'tuto', 'svou', 'nám']
verbs = ["být","bejt","jsem","sme","jsi","je","jest","jsme","jste","jsou","budu","budeš","bude","budeme","budete","budou","buď","budiž","buďme","buďmež","buďte","buďtež","byl","byla","bylo","byli","byly","jsa","jsouc","jsouce","byv","byvše","byvši","bych","bychom","nebyla","nebylo","nam","vás","vas","chtěli","chteli","dali","bys","byste","by", "seš", "mám","máš","má","máme","máte","mají","měj","mějme","mějte","měl","měla","mělo","měli","měly","maje","majíc","majíce"]
another_specific = ["jít","přes","muset","jeden","druhý","moct","opravdu","všechen","mít","moc","dostat","dal","chtít","dát","si","cca","dne","jen","mi","mě","tady","tomu","že","to","nám","ná","takže","jako","už","pokud","asi","celkem","docela","tam","ze","ve","ji","ta","pak","taky","což","tím","již","možná","která","toho","protože","sem","kde","která","které","tu","než","když","Kč","při","až","ho","této","mne","aby","tuto","tom","No","kdy","jejich","jinak","zde","kterou","toto","ní","nás","mu","dostali","objednali","jím","myslím","jim","Já","Jen","námi","mě","me","Na","Po","není",")","(",".",",",":","!","...","-","?"]

#STOPWORDS WITHOUT DIACRITICS LOWERCASE
prepositions_without = [''.join((c for c in unicodedata.normalize('NFD', preposition) if unicodedata.category(c) != 'Mn')) for preposition in prepositions]
pronouns_without = [''.join((c for c in unicodedata.normalize('NFD', pronoun) if unicodedata.category(c) != 'Mn')) for pronoun in pronouns]
conjunctions_without = [''.join((c for c in unicodedata.normalize('NFD', conjunction) if unicodedata.category(c) != 'Mn')) for conjunction in conjunctions]
others_without = [''.join((c for c in unicodedata.normalize('NFD', other) if unicodedata.category(c) != 'Mn')) for other in others]
verbs_without = [''.join((c for c in unicodedata.normalize('NFD', verb) if unicodedata.category(c) != 'Mn')) for verb in verbs]

#STOPWORDS WITH DIACRITICS UPPERCASE
prepositions_upper = [preposition.upper() for preposition in prepositions]
conjuctions_upper = [conjuction.upper() for conjuction in conjunctions]
pronouns_upper = [pronoun.upper() for pronoun in pronouns]
others_upper = [other.upper() for other in others]
verbs_upper = [verb.upper() for verb in verbs]

#STOPWORDS WITHOUT DIACRITICS UPPERCASE
prepositions_upper_without = [preposition.upper() for preposition in prepositions_without]
conjuctions_upper_without = [conjuction.upper() for conjuction in conjunctions_without]
pronouns_upper_without = [pronoun.upper() for pronoun in pronouns_without]
others_upper_without = [other.upper() for other in others_without]
verbs_upper_without = [verb.upper() for verb in verbs_without]

stopwords_cz = verbs + verbs_without + verbs_upper + verbs_upper_without + another_specific + others + others_without + others_upper + others_upper_without + prepositions + conjunctions + pronouns + prepositions_without + pronouns_without + conjunctions_without + prepositions_upper + conjuctions_upper + pronouns_upper + prepositions_upper_without + conjuctions_upper_without + pronouns_upper_without

extract_re = re.compile(r'^.*\.+.*$')
for extract in extracts_prev:
    for i in extract:
        if len(i) < 4:
            extract.remove(i)
        elif i.endswith('.') or extract_re.match(i) or i in stopwords_cz:
            extract.remove(i)

for extract in extracts_next:
    for i in extract:
        if len(i) < 4:
            extract.remove(i)
        elif i.endswith('.') or i == extract_re.match(i) or i in stopwords_cz:
            extract.remove(i)

#SKAREDY KOD PRO ROZDELENI UTRZKU PODLE TEMAT A ZJISTENI NEJCASTEJSICH SLOV

def words_to_dict(keyword,list_name,dict_name,prev_or_next):

    for extract in prev_or_next:
        if key_word in extract:
            list_name.append(extract)

    for extract in list_name:
        for word in extract:
            if word == keyword:
                pass
            elif word in stopwords_cz:
                pass
            elif word in dict_name:
                dict_name[word] += 1
            else:
                dict_name[word] = 1

    dict_name = sorted(dict_name.items(), key=lambda kv: kv[1], reverse=True)
    return dict_name


def to_csv(keyword,dictionary_prev,dictionary_next):
    to_file = ''
    next_dict = ''
    n = 0
    with open("frequent_words.csv","a",encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for i in dict_prev:
            try:
                i = str(i)
                next_dict = str(dict_next[n])
                to_file = (i.replace(',', '#').replace('()', ''), key_word, next_dict.replace('""', '').replace(',', '#').replace('()', ''))
                writer.writerow(to_file)
                n += 1
            except IndexError:
                pass



for key_word in key_words:
    list_prev = []
    dict_prev = {}
    list_next = []
    dict_next = {}
    dict_prev = words_to_dict(key_word,list_prev,dict_prev,extracts_prev)
    dict_next = words_to_dict(key_word,list_next,dict_next,extracts_next)
    to_csv(key_word,dict_prev,dict_next)
