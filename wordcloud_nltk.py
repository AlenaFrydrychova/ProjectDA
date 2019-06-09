import xlrd
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import unicodedata
import random
import sys
"""
#OTEVIRANI SOUBORU POMOCI KNIHOVNY XLRD, ROZDELENI OBSAHU PODLE RADKU
path_to_sentiment_xlsx = sys.argv[1]
workbook = xlrd.open_workbook(path_to_sentiment_xlsx, 'rb')
#C:\Users\Alena\Documents\DA Czechitas\projekt\ProjectDA\Excel\sentiment.xlsx'
# C:\DA\ProjectDA\Excel\sentiment.xlsx
sheet = workbook.sheet_by_index(0)
rows = []
for i in range(sheet.nrows):
    columns = []
    for j in range(sheet.ncols):
        columns.append(sheet.cell(i, j).value)
    rows.append(columns)

# VYTAHNE Z RADKU 2. HODNOTU - REVIEW A ROZDELÍ PODLE SENTIMENTU DO SEZNAMŮ
reviews_all = []
positive_reviews = []
negative_reviews = []
neutral_reviews = []
for i in rows[1:]:
    reviews_all.append(i[1])
    if i[2] == 1:
        positive_reviews.append(i[1])
    elif i[2] == 0:
        neutral_reviews.append(i[1])
    elif i[2] == -1:
        negative_reviews.append(i[1])
"""
#STOPWORDS WITH DIACRITICS LOWERCASE
prepositions = ["od","ke","z","s","do","bez","krom","kromě","podle","okolo","vedle","během","prostřednictvím","u","za","k","před","na","oproti","naproti","proti","pro", "mimo", "pod","nad","mezi","skrz","o","po","v"]
conjunctions = ["a", "i", "ani", "nebo", "či", "přímo", "nadto", "ani", "jak", "tak", "hned", "jednak", "zčásti", "dílem", "ale", "avšak", "však", "leč", "nýbrž", "naopak", "jenomže", "jenže", "sice", "jistě", "ale", "i", "ba", "ba i", "ba ani", "nadto", "dokonce", "nejen", "nebo", "anebo", "buď", "totiž", "vždyť", "neboť", "vždyť", "totiž", "však", "také", "proto", "a proto", "a tak", "tudíž", "a tudíž", "tedy"]
pronouns = ["já", "ty", "on", "ona", "ono", "my", "vy", "oni", "ony", "ona","se", "můj", "tvůj", "jeho", "její", "náš", "váš", "svůj", "ten", "tento", "tenhle", "onen", "takový", "týž", "tentýž", "sám", "kdo", "co", "jaký", "který","čí", "jenž", "nikdo", "nic", "nijaký", "ničí", "žádný", "někdo", "nějaký", "některý", "lecco", "něčí", "něco"]
verbs = ["být","bejt","jsem","sme","jsi","je","jest","jsme","jste","jsou","budu","budeš","bude","budeme","budete","budou","buď","budiž","buďme","buďmež","buďte","buďtež","byl","byla","bylo","byli","byly","jsa","jsouc","jsouce","byv","byvše","byvši","bych","bychom","nebyla","nebylo","nam","vás","vas","chtěli","chteli","dali","bys","byste","by", "seš", "mám","máš","má","máme","máte","mají","měj","mějme","mějte","měl","měla","mělo","měli","měly","maje","majíc","majíce"]
another_specific = ["jít","přes","muset","jeden","druhý","moct","opravdu","všechen","mít","moc","dostat","dal","chtít","dát","si","cca","dne","jen","mi","mě","tady","tomu","že","to","nám","ná","takže","jako","už","pokud","asi","celkem","docela","tam","ze","ve","ji","ta","pak","taky","což","tím","již","možná","která","toho","protože","sem","kde","která","které","tu","než","když","Kč","při","až","ho","této","mne","aby","tuto","tom","No","kdy","jejich","jinak","zde","kterou","toto","ní","nás","mu","dostali","objednali","jím","myslím","jim","Já","Jen","námi","mě","me","Na","Po","není",")","(",".",",",":","!","...","-","?"]
text_specific_stopwords = ["jídlo","jídla","jidlo","jidla","jídel","jídlu","obsluha","obsluhy","obsluhu","restaurace","restauraci","objednat"]

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
stopwords_cz = prepositions + conjunctions + pronouns + verbs + prepositions_without + pronouns_without + conjunctions_without + verbs_without + prepositions_upper + conjuctions_upper + pronouns_upper + verbs_upper + prepositions_upper_without + conjuctions_upper_without + pronouns_upper_without + verbs_upper_without + another_specific + text_specific_stopwords

#WORDCLOUD
def wordcloud_color(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h = color
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)
    return "hsl({}, {}%, {}%)".format(h, s, l)

def wordcloud_to_file(list_of_text,file):
    list_of_text = [review.strip() for review in list_of_text]
    reviews_dict = {"review" : list_of_text}
    df = pd.DataFrame(reviews_dict)
    text = " ".join(review for review in df.review) #recenze
    wordcloud = WordCloud(width=600, height=800,color_func=wordcloud_color, stopwords=stopwords_cz, max_words=50, background_color="white").generate(text)
    wordcloud.to_file("img\\" + file)

#LEMMATIZOVANÉ REVIEWS
path_to_lemmata_xlsx = sys.argv[1]
workbook = xlrd.open_workbook(path_to_lemmata_xlsx, 'rb')
# Andy -> C:\DA\ProjectDA\Excel\lemmata_reviews.xlsx

sheet = workbook.sheet_by_index(0)
rows = []
for i in range(sheet.nrows):
    columns = []
    for j in range(sheet.ncols):
        columns.append(sheet.cell(i, j).value)
    rows.append(columns)

lemma_reviews_all = []
lemma_neutral_reviews = []
lemma_positive_reviews = []
lemma_negative_reviews = []
for i in rows[1:]:
    lemma_reviews_all.append(i[1])
    if i[2] == 1:
        lemma_positive_reviews.append(i[1])
    elif i[2] == 0:
        lemma_neutral_reviews.append(i[1])
    elif i[2] == -1:
        lemma_negative_reviews.append(i[1])

color = 60
#wordcloud_to_file(reviews_all,"all_reviews.png")
#wordcloud_to_file(lemma_reviews_all,"lemma_all_reviews.png")
color = 140
#wordcloud_to_file(positive_reviews,"positive_reviews.png")
#wordcloud_to_file(lemma_positive_reviews,"lemma_positive_reviews.png")
wordcloud_to_file(lemma_positive_reviews,"wordcloud_positive_presentation.png")
color = 21
#wordcloud_to_file(negative_reviews,"negative_reviews.png")
#wordcloud_to_file(lemma_negative_reviews,"lemma_negative_reviews.png")
wordcloud_to_file(lemma_negative_reviews,"wordcloud_negative_presentation.png")


#KNIHOVNA NLTK
import nltk
from nltk.tokenize import word_tokenize
from nltk.text import Text
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
"""
def get_concordance(list_of_reviews,concordance_word,count_of_lines,file):
    string_reviews = "\n".join(list_of_reviews)
    tokens = nltk.tokenize.word_tokenize(string_reviews)
    tokens = [token for token in tokens if not token in stopwords_cz]
    clean_reviews = " ".join(tokens)
    #Zobrazení shody ukazuje každý výskyt daného slova spolu s určitým kontextem
    t = nltk.WhitespaceTokenizer()
    textList = Text(t.tokenize(string_reviews))
    #zápis do souboru (přesměruje výsledek printu do souboru)
    sys.stdout = open("txt\\" + file, 'a', encoding="utf-8")
    textList.concordance(concordance_word, lines=count_of_lines)
    #vrátí výsledky printu do příkazové řádky
    sys.stdout = sys.__stdout__
#JE TŘEBA PREVEST REVIEWS NA LOWER CASE, TAKHLE TO NAJDE JEN VÝSKYTY PŘEŠNĚ PODLE TOHO JAK SLOVO ZADÁM
get_concordance(positive_reviews,"obsluha",2000,"obsluha_concordance_positive.txt")
get_concordance(negative_reviews,"obsluha",2000,"obsluha_concordance_negative.txt")
get_concordance(reviews_all,"obsluha",2000,"obsluha_concordance_all.txt")

get_concordance(positive_reviews,"restaurace",2000,"restaurace_concordance_positive.txt")
get_concordance(negative_reviews,"restaurace",2000,"restaurace_concordance_negative.txt")
get_concordance(reviews_all,"restaurace",2000,"restaurace_concordance_all.txt")

get_concordance(positive_reviews,"jídlo",2000,"jídlo_concordance_positive.txt")
get_concordance(negative_reviews,"jídlo",2000,"jídlo_concordance_negative.txt")
get_concordance(reviews_all,"jídlo",2000,"jídlo_concordance_all.txt")

"""
"""
#lexikální bohatost textu neboli počet odlišných slov v textu (v procentech)
richness = (len(set(textList)) / len(textList))*100
print(round(richness,2), "%")
"""
"""
#FREKVENCE SLOV (potřeba lemmatizovat alespoň některá a zapsat je do nějaké tabulky, ideální by bylo udělat zvlášť frekvenci slov pro pozitivní a negativní recenze, stejně tak wordcloud, který je momentálně ze všech recenzí)
def get_frequent_words(list_of_words, file):
    string_reviews = "\n".join(list_of_words)
    tokens = nltk.tokenize.word_tokenize(string_reviews)
    tokens = [token for token in tokens if not token in stopwords_cz]
    clean_reviews = " ".join(tokens)
    fdist = FreqDist()
    for word in word_tokenize(clean_reviews):
        fdist[word.lower()] += 1
    words = fdist.most_common(100)

    df = pd.DataFrame(words ,columns=["word","count"])
    export_csv = df.to_csv ("C:\\DA\\ProjectDA\\csv\\" + file, index = None, header=True)

get_frequent_words(lemma_reviews_all, "frequent_words_all.csv")
get_frequent_words(lemma_positive_reviews, "frequent_words_positive.csv")
get_frequent_words(lemma_negative_reviews, "frequent_words_negative.csv")
"""
