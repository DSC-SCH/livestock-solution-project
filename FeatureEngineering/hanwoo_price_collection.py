import pandas as pd
import os
import datetime
import csv
import pymysql

os.chdir(r"C:\Users\a0105\Desktop\DSC\ddd\data")

col_names = ['경락일자', '경락요일', '1++', '1+', 'except0', '1', '2', '3', 'A', 'B', 'C', '전체', 'except1', '상승하강', '가격',
             'except2']
col_names2 = ['경락일자', '경락요일', '1++', '1+', '1', '2', '3', 'A', 'B', 'C', '전체', 'except1', '상승하강', '가격', 'except2']

df2 = []

for i in range(1, 177): # page 수 176

    try:
        df = pd.read_excel("01_1. 축산물 실시간 가격_total.xlsx", skiprows=1, sheet_name='Page ' + str(i), names=col_names)
        df = df.drop(['except0'], axis=1)

    except:
        df = pd.read_excel("01_1. 축산물 실시간 가격_total.xlsx", skiprows=1, sheet_name='Page ' + str(i), names=col_names2)

    df2.append(df)

data2 = pd.concat(df2)

# 데이터 기간: 2001.01.01~2020.06.05
data2 = data2.reset_index()
data2 = data2.drop(['index'],axis=1)
data2

data2 = data2[(data2['경락요일']!='(일)')&(data2['경락요일']!='(토)')]
data2 = data2[['경락일자','전체']]

data2 = data2.sort_values(by=['경락일자'])
data2 = data2.reset_index()
del data2['index']

data2.columns = ['date','price']
data2['place'] = '전국'

data2['date'] = pd.to_datetime(data2['date'])
data2['date']

data2['date'] = pd.to_datetime(data2['date'], format = '%Y-%-m-%d')
data2.to_csv('hanwoo_price.csv',encoding = 'utf-8-sig')

f = open('hanwoo_price.csv', 'r', encoding='utf-8-sig')

csvReader = csv.reader(f)

db = pymysql.connect(host='localhost', user = 'root', password = '#',db='ddd' )
curs = db.cursor()

all(next(csvReader) for i in range(1))

for row in csvReader:
    date = (row[0])

    price = (row[1])

    place = (row[2])

    print(date)s

    print(price)

    print(place)

    query = "INSERT IGNORE INTO hanwoo_price(date, price, place) VALUES(%s,%s,%s)"
    print(query)
    curs.execute(query, (date, price, place))

db.commit()
db.close()
