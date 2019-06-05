import sys
import xlrd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import csv
import numpy as np
from collections import Counter
import pandas as pd

path = sys.argv[1]
#OTEVIRANI SOUBORU POMOCI KNIHOVNY XLRD, ROZDELENI OBSAHU PODLE RADKU
workbook = xlrd.open_workbook(path, 'rb')
#Andy -> C:\DA\ProjectDA\Excel\sentiment.xlsx

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

plt.scatter(reviews_len, sentiment, marker='o')
plt.ylabel('sentiment')
plt.xlabel('délka recenze')
plt.title('sentiment vs. délka recenze')
plt.show()

"""
politeness_values = []
rude_words = []
with open("csv\\politeness_of_negative_reviews.csv","r", encoding ="utf-8") as f:
    csvreader = csv.reader(f, delimiter=',')
    for row in csvreader:
        politeness_values.append(row[1])
        rude_words.append(row[2])

#rude_words = list(filter(None, rude_words))
#print(rude_words)

D = Counter(politeness_values) #spočítá hodnoty jednotlivých proměnných
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), list(D.keys()))
plt.ylabel('Count')
plt.title('Slušnost negativních recenzí')
plt.show()
print(pd.DataFrame.from_dict(D, orient='index', columns = ["count"]))
"""
