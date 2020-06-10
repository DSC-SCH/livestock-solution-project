import pandas as pd
import pymysql
import numpy as np

# data추출
def select_all_price():
    conn = pymysql.connect(host='localhost', user = 'root', password = '#',db='ddd')
    try:
        with conn.cursor() as curs:
            sql = "select * from hanwoo_price"
            curs.execute(sql)
            rs = curs.fetchall()
            date = []
            place = []
            price = []

            for row in rs:
                date.append(row[0])
                place.append(row[1])
                price.append(row[2])

            date_df = pd.DataFrame(date, columns=['date'])
            place_df = pd.DataFrame(place, columns=['place'])
            price_df = pd.DataFrame(price, columns=['price'])

            data = pd.concat([date_df,place_df,price_df],axis=1)

            data = data[data['place']=='전국']
            data = data.drop(['place'], axis = 1)

    finally:
        conn.close()

    return data


# 주간데이터로 변환
def week_price(data):

    data['price'] = data['price'].replace('[-=.#/?:$}]','',regex=True)
    data['price'] = data['price'].replace('',np.nan,regex=True)

    data = data.fillna(method='ffill')
    data['price'] = data['price'].astype('int')

    day_7 = pd.date_range(start=data['date'][0], end=data['date'][len(data) - 1], freq='W')  # 주별 데이터 생성
    day_7 = pd.to_datetime(day_7, format="%Y-%m-%d")
    day_7 = pd.DataFrame(day_7, columns=['week_date'])

    price_7 = []

    for x in range(len(day_7) - 1):
        a = []
        for i in range(len(data)):
            if data['date'][i] >= day_7['week_date'][x] and data['date'][i] < day_7['week_date'][x + 1]:
                a.append(data['price'][i])
        price_7.append(np.mean(a))

    price_7 = pd.DataFrame(price_7, columns=['price_mean'])
    price_processing = pd.concat([day_7, price_7], axis=1)

    return price_processing

data = week_price(select_all_price())  # 주간 데이터 저장 (DB에 저장해야함)
