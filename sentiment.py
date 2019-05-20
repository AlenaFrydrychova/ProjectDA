import requests
import csv
import xlrd

def get_sentiment(chunk):
    payload = {
        'text': chunk,
        'user_key': 'b0273bf8e53597cc65ddaab58d6ad530'
    }
    r = requests.get('https://api.geneea.com/s2/sentiment', params=payload)
    return(r.json())


def analyzuj_recenzi(reviews, recenze):
	hodnoty = []

	for recenze in reviews[:10]:
		try:
			hodnoty.append(get_sentiment(recenze)['sentiment'])
		except KeyError:
			pass
	return(hodnoty)

workbook = xlrd.open_workbook('C:\\Users\\Alena\\Documents\\Da Czechitas\\projekt\\ProjectDA\\reviews.xlsx', 'rb')
sheet = workbook.sheet_by_index(0)
rows = []
for i in range(sheet.nrows):
    columns = []
    for j in range(sheet.ncols):
        columns.append(sheet.cell(i, j).value)
    rows.append(columns)


reviews = []
for i in rows[1:]:
    reviews.append(i[2])


hodnoty_tofile = []
for recenze in reviews:
    print(recenze, analyzuj_recenzi(reviews, recenze))



with open('sentiment.csv', 'w', encoding='utf-8') as csvfile:
	writer = csv.writer(csvfile)
	for value in hodnoty_tofile:
		writer.writerow([value])