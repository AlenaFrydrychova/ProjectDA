import xlrd
import requests
import json
import csv
import unicodedata
import time
import sys

path_to_sentiment_xlsx = sys.argv[1]
#do příkazové řádky je třeba napsat příkaz ve formě -> nazev souboru cesta
#Andy -> morphological_analysis.py C:\\DA\\ProjectDA\\Excel\\sentiment.xlsx
#ALena -> morphological_analysis.py C:\\Users\\Alena\\Documents\\DA_Czechitas\\projekt\\ProjectDA\\Excel\\sentiment.xlsx

#OTEVIRANI SOUBORU POMOCI KNIHOVNY XLRD, ROZDELENI OBSAHU PODLE RADKU
workbook = xlrd.open_workbook(path_to_sentiment_xlsx, 'rb')

sheet = workbook.sheet_by_index(0)
rows = []
for i in range(sheet.nrows):
    columns = []
    for j in range(sheet.ncols):
        columns.append(sheet.cell(i, j).value)
    rows.append(columns)

#STOPWORDS WITH DIACRITICS LOWERCASE
prepositions = ["od","z","s","do","bez","krom","kromě","podle","okolo","vedle","během","prostřednictvím","u","za","k","před","na","oproti","naproti","proti","pro", "mimo", "pod","nad","mezi","skrz","o","po","v"]
conjunctions = ["a", "i", "ani", "nebo", "či", "přímo", "nadto", "ani", "jak", "tak", "hned", "jednak", "zčásti", "dílem", "ale", "avšak", "však", "leč", "nýbrž", "naopak", "jenomže", "jenže", "sice", "jistě", "ale", "i", "ba", "ba i", "ba ani", "nadto", "dokonce", "nejen", "nebo", "anebo", "buď", "totiž", "vždyť", "neboť", "vždyť", "totiž", "však", "také", "proto", "a proto", "a tak", "tudíž", "a tudíž", "tedy"]
pronouns = ["já", "ty", "on", "ona", "ono", "my", "vy", "oni", "ony", "ona","se", "můj", "tvůj", "jeho", "její", "náš", "váš", "svůj", "ten", "tento", "tenhle", "onen", "takový", "týž", "tentýž", "sám", "kdo", "co", "jaký", "který","čí", "jenž", "nikdo", "nic", "nijaký", "ničí", "žádný", "někdo", "nějaký", "některý", "lecco", "něčí", "něco"]
verbs = ["být","bejt","jsem","jsi","je","jest","jsme","jste","jsou","budu","budeš","bude","budeme","budete","budou","buď","budiž","buďme","buďmež","buďte","buďtež","byl","byla","bylo","byli","byly","jsa","jsouc","jsouce","byv","byvše","byvši","bych","bychom","bys","byste","by", "seš", "mám","máš","má","máme","máte","mají","měj","mějme","mějte","měl","měla","mělo","měli","měly","maje","majíc","majíce"]
another_specific = ["si","nebylo","nebyla","cca","dne","jen","mi","mě","tady","tomu","že","to","nám","ná","takže","jako","už","pokud","asi","celkem","docela","tam","dali","ze","ve","ji","ta","pak","taky","což","tím","již","možná","která","toho","protože","sem","kde","která","které","tu","než","když","Kč","při","až","ho","této","mne","aby","nebyl","tuto","tom","No","kdy","dal","nebyla","jejich","jinak","zde","kterou","toto","dala","ní","nás","mu","dostali","objednali","jím","myslím","jim","Já","Jen","námi","Na","Po","není",")","(",".",",",":","!","...","-","?"]

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

# ALL STOPWORDS
stopwords_cz = prepositions + conjunctions + pronouns + verbs + prepositions_without + pronouns_without + conjunctions_without + verbs_without + prepositions_upper + conjuctions_upper + pronouns_upper + verbs_upper + prepositions_upper_without + conjuctions_upper_without + pronouns_upper_without + verbs_upper_without + another_specific

# VYTAHNE Z RADKU 2. HODNOTU - REVIEW A ROZDELÍ PODLE SENTIMENTU DO SEZNAMŮ
reviews_all = []
sentiment_all = []
positive_reviews = []
negative_reviews = []
neutral_reviews = []
review_id_negative = []
for i in rows[1:]:
    sentiment_all.append(i[2])
    reviews_all.append(i[1])
    if i[2] == 1:
        positive_reviews.append(i[1])
    elif i[2] == 0:
        neutral_reviews.append(i[1])
    elif i[2] == -1:
        negative_reviews.append(i[1])
        review_id_negative.append(i[0])

#split reviews that are logner than 1000characters
all_reviews_after_splitting = []
reviews_all_id = []
id = 1
for review in reviews_all:
    number_of_characters = 950
    split_review = []
    if len(review) > number_of_characters:
        for i in range(0, len(review), number_of_characters):
            all_reviews_after_splitting.append(review[i:i+number_of_characters])
            reviews_all_id.append(id)
        id += 1
    else:
        all_reviews_after_splitting.append(review)
        reviews_all_id.append(id)
        id += 1
"""
#request na API na FI MU
i = 2400 #musí se rovnat začátku rozsahu ve for cyklu níže (nelekat se, nebude se to rovnat tomu jaké id je v souboru lemmata.csv naposledy)
for text in all_reviews_after_splitting[2400:2500]:
    url = "https://nlp.fi.muni.cz/languageservices/"
    morphological_analysis = "service.py?call=tagger&lang=cs&output=json&text="
    res = requests.get(url + morphological_analysis + text, timeout=5)
    cont = res.json()
     #seznam seznamů ve slovníku vertical, lemmata jsou vždy na 1 místě v každém seznamu
    #přidá lemmata slov, která nejsou ve stopslovech do listu, juhů
    try:
        #někdy neexistuje, nenajde lemma ke slovu
        list_of_words = cont["vertical"]
    except (KeyError,NameError):
        pass
    try:
        for list in list_of_words:
            #někdy není lemma, nastal by indexerror
            try:
                if list[1] not in stopwords_cz and len(list[1]) > 2: #podminka pro stopslova a kratší slova než tři znaky
                    with open("csv\\lemmata.csv","a",encoding="utf-8", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([round(reviews_all_id[i])]+[list[1]])
            except IndexError:
                pass
    except NameError:
        print("Too many calls per day")
        break
    i += 1
    time.sleep(1)
"""
#POLITENESS (asi nemá smysl, četla jsem recenze, a asi tak dvě by mohly být "rude", některé navíc mají více než tisíc znaků, takže nejdou poslat)
i = 0 #neodpovídá skutečnosti, protože bere jen z negativních recenzí
for text in negative_reviews[0:]: #nevím proč to nějaké vynechává
    url = "https://nlp.fi.muni.cz/languageservices/"
    politeness_of_text = "service.py?call=polite&lang=cs&output=json&text=" + text
    res = requests.get(url + politeness_of_text + text, timeout=(60,60))
    cont = res.json()
    try:
        politeness_of_review = cont.get("politeness")
        rude_words = cont.get("rudewords")
    except KeyError:
        politeness_of_review = "error"
        rude_words = "error"
    with open("csv\\politeness_of_negative_reviews.csv","a",encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([review_id_negative[i]]+[politeness_of_review]+[rude_words])
    i += 1
    time.sleep(1)
