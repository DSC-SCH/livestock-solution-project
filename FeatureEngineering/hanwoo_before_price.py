import csv
import pymysql

f = open('data/hanwoo_price.csv', 'r', encoding='utf-8-sig')

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