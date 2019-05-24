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
