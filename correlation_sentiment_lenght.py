import sys
import xlrd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

path = sys.argv[1]
#OTEVIRANI SOUBORU POMOCI KNIHOVNY XLRD, ROZDELENI OBSAHU PODLE RADKU
workbook = xlrd.open_workbook(path, 'rb')
#Andy -> C:\\DA\\ProjectDA\\Excel\\sentiment.xlsx

sheet = workbook.sheet_by_index(0)
rows = []
for i in range(sheet.nrows):
    columns = []
    for j in range(sheet.ncols):
        columns.append(sheet.cell(i, j).value)
    rows.append(columns)

sentiment = []
reviews_len = []

for i in rows[1:]:
    sentiment.append(i[2])
    reviews_len.append(i[3])


plt.scatter(reviews_len, sentiment, marker='o', c="b");
plt.show()
