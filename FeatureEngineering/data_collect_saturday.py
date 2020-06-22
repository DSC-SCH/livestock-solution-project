# -*- coding: utf-8 -*-

from lxml import etree

import xml.etree.ElementTree as ElementTree
import pandas as pd  # 1.0.3 version
import datetime

from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib
import requests
from bs4 import BeautifulSoup as bs
import time
import pymysql
from sqlalchemy import create_engine
import numpy as np

engine = create_engine("mysql+mysqldb://root:" + "password" + "@localhost/ddd", encoding='utf-8')
conn = engine.connect()

# -------------------------------------------------------------
# hanwoo price 데이터 수집
# -------------------------------------------------------------
now = datetime.datetime.now()

crawl_dates = pd.date_range(start=now - datetime.timedelta(5), end=now - datetime.timedelta(1))
crawl_dates = crawl_dates.strftime("%Y%m%d").tolist()

place_df = []
date_df = []
price_df = []

for date_ in crawl_dates:
    # service key 발급받은 후 # 을 변경
    request = urllib.request.Request(
        "http://data.ekape.or.kr/openapi-data/service/user/grade/liveauct?serviceKey=#&auctDate=" + str(
            date_) + "&auctFlag=2")

    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()

    tree = etree.fromstring(response_body)

    for media in tree.getiterator('item'):
        place = media.findtext("abattNm")
        date = media.findtext("auctDate")
        price = media.findtext("hanwooAuctAmt")
        
        place_df.append(place)
        date_df.append(date)
        price_df.append(price)
        
data_price = pd.DataFrame({'date': date_df, 'place': place_df, 'price': price_df})
data_price = data_price.fillna(method='ffill')

data_price.to_sql(name='hanwoo_price', con=engine, index=False, if_exists="append")
conn.close()
     
# -------------------------------------------------------------
# 기상 관측 데이터 수집
# -------------------------------------------------------------

url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList?serviceKey=#'

# w지역별 코드
stnlds = [90, 93, 95, 98, 99, 100, 101, 102, 104, 105, 106, 108, 112, 114, 115, 119,
          121, 127, 129, 130, 131, 133, 135, 136, 137, 138, 140, 143, 146, 152, 155,
          156, 159, 162, 165, 168, 169, 170, 172, 174, 177, 184, 185, 188, 189, 192,
          201, 202, 203, 211, 212, 216, 217, 221, 226, 232, 235, 236, 238, 243, 244,
          245, 247, 248, 251, 252, 253, 254, 255, 257, 258, 259, 260, 261, 262, 263,
          264, 266, 268, 271, 272, 273, 276, 277, 278, 279, 281, 283, 284, 285, 288,
          289, 294, 295]

# Attribute마다 담을 빈 리스트 할당
stnld_lst = []
date_lst = []
avg_ta_lst = []
max_ta_lst = []
min_ta_lst = []
sum_rn_lst = []
sum_sshr_lst = []
max_insws_lst = []
max_ws_lst = []
sum_gsr_lst = []
avg_ts_lst = []
min_rhm_lst = []
avg_rhm_lst = []
avg_ws_lst = []
hr1_maxicsr_lst = []

# weather data collect
for stnld in stnlds:

    uri = url + "&numOfRows=10" + f"&pageNo=1" + "&dataCd=ASOS" + "&dateCd=DAY" + f"&startDt={crawl_dates[0]}" + f"&endDt={crawl_dates[-1]}" + f"&stnIds={stnld}"
    res = requests.get(uri)
    time.sleep(3)
    soup = bs(res.content, 'html.parser')
    items = soup.select('item')

    for item in items:

        date = item.select_one('tm').text
        avg_ta = item.select_one('avgta')
        if avg_ta is None:
            avg_ta = None
        else:
            avg_ta = avg_ta.text
        max_ta = item.select_one('maxta')
        if max_ta is None:
            max_ta = None
        else:
            max_ta = max_ta.text
        min_ta = item.select_one('minta')
        if min_ta is None:
            min_ta = None
        else:
            min_ta = min_ta.text
        sum_rn = item.select_one('sum_rn')
        if sum_rn is None:
            sum_rn = None
        else:
            sum_rn = sum_rn.text
        sum_sshr = item.select_one('sumsshr')
        if sum_sshr is None:
            sum_sshr = None
        else:
            sum_sshr = sum_sshr.text
        max_insws = item.select_one('maxinsws')
        if max_insws is None:
            max_insws = None
        else:
            max_insws = max_insws.text
        max_ws = item.select_one('maxws')
        if max_ws is None:
            max_ws = None
        else:
            max_ws = max_ws.text
        sum_gsr = item.select_one('sumgsr')
        if sum_gsr is None:
            sum_gsr = None
        else:
            sum_gsr = sum_gsr.text
        avg_ts = item.select_one('avg_ts')
        if avg_ts is None:
            avg_ts = None
        else:
            avg_ts = avg_ts.text
        min_rhm = item.select_one('minrhm')
        if min_rhm is None:
            min_rhm = None
        else:
            min_rhm = min_rhm.text
        avg_rhm = item.select_one('avgrhm')
        if avg_rhm is None:
            avg_rhm = None
        else:
            avg_rhm = avg_rhm.text
        avg_ws = item.select_one('avgws')
        if avg_ws is None:
            avg_ws = None
        else:
            avg_ws = avg_ws.text
        hr1_maxicsr = item.select_one('hr1maxicsr')
        if hr1_maxicsr is None:
            hr1_maxicsr = None
        else:
            hr1_maxicsr = hr1_maxicsr.text

        # 변수명에 맞게 각 리스트에 담기
        stnld_lst.append(stnld)
        date_lst.append(date)
        avg_ta_lst.append(avg_ta)
        max_ta_lst.append(max_ta)
        min_ta_lst.append(min_ta)
        sum_rn_lst.append(sum_rn)
        sum_sshr_lst.append(sum_sshr)
        max_insws_lst.append(max_insws)
        max_ws_lst.append(max_ws)
        sum_gsr_lst.append(sum_gsr)
        avg_ts_lst.append(avg_ts)
        min_rhm_lst.append(min_rhm)
        avg_rhm_lst.append(avg_rhm)
        avg_ws_lst.append(avg_ws)
        hr1_maxicsr_lst.append(hr1_maxicsr)

data_weather = pd.DataFrame(
    {'date': date_lst, 'avg_ta': avg_ta_lst, 'max_ta': max_ta_lst, 'min_ta': min_ta_lst, 'sum_rn': sum_rn_lst,
     'sum_sshr': sum_sshr_lst, 'max_insws': max_insws_lst, 'max_ws': max_ws_lst, 'sum_gsr': sum_gsr_lst,
     'avg_ts': avg_ts_lst,
     'min_rhm': min_rhm_lst, 'avg_rhm': avg_rhm_lst, 'avg_ws': avg_ws_lst, 'hr1_maxicsr': hr1_maxicsr_lst})

data_weather = data_weather.fillna(method='ffill')

engine = create_engine("mysql+mysqldb://root:" + "password" + "@localhost/ddd", encoding='utf-8')
conn = engine.connect()

data_weather.to_sql(name='weather', con=engine, index=False, if_exists="append")

conn.close()
# -------------------------------------------------------------
# hanwoo price 데이터 전처리
# -------------------------------------------------------------
# hanwoo price 주간데이터로 변환

data_price = data_price[data_price['place'] == '전국']
data_price = data_price.drop(['place'], axis=1)

data_price = data_price.reset_index()
del data_price['index']

data_price['price'] = data_price['price'].astype('int')

data_price['date'] = pd.to_datetime(data_price['date'], format = '%Y-%m-%d')

day_7 = pd.date_range(start=data_price['date'][0]-datetime.timedelta(1), end=data_price['date'][len(data_price) - 1]+datetime.timedelta(7), freq='W')  # 주별 데이터 생성
day_7 = pd.to_datetime(day_7, format="%Y-%m-%d")
day_7 = pd.DataFrame(day_7, columns=['week_date'])

price_7 = []

for x in range(len(day_7) - 1):
    a = []
    for i in range(len(data_price)):
        if data_price['date'][i] >= day_7['week_date'][x] and data_price['date'][i] < day_7['week_date'][x + 1]:
            a.append(data_price['price'][i])
    price_7.append(np.mean(a))

price_7 = pd.DataFrame(price_7, columns=['price_mean'])
price_processing = pd.concat([day_7, price_7], axis=1)  # hanwoo price week data

price_processing = price_processing.iloc[0:len(price_processing)-1]
# -------------------------------------------------------------
# 기상관측 데이터 전처리
# -------------------------------------------------------------

features = ['avg_ta', 'max_ta', 'min_ta', 'sum_rn', 'sum_sshr', 'max_insws', 'max_ws', 'sum_gsr', 'avg_ts', 'min_rhm',
            'avg_rhm', 'avg_ws', 'hr1_maxicsr']

# data type이 object로 들어가있으므로 수정 필요
data_weather[features] = data_weather[features].astype(float)

data_group = data_weather.groupby(['date']).mean()

data_group.index = pd.to_datetime(data_group.index, format = '%Y-%m-%d')

day_7 = pd.date_range(start=data_group.index[0]-datetime.timedelta(1), end=data_group.index[len(data_group) - 1]+datetime.timedelta(7), freq='W')  # 주별 데이터 생성    
day_7 = pd.to_datetime(day_7, format="%Y-%m-%d")
day_7 = pd.DataFrame(day_7, columns=['week_date'])

def mean_week(col_):

    avg_7 = []

    for x in range(len(day_7['week_date']) - 1):

        a = []

        for i in range(len(data_group.index)):

            if data_group.index[i] >= day_7['week_date'][x] and data_group.index[i] < day_7['week_date'][x + 1]:
                a.append(col_[i])

        avg_7.append(np.mean(a))

    return avg_7


df = pd.DataFrame()

for col_name in features:
    df[col_name] = mean_week(data_group[col_name])

df = pd.concat([day_7, df], axis=1)

weather_processing = df.iloc[0:len(df)-1]

final_data = pd.merge(price_processing, weather_processing, how='inner', on=['week_date'])

engine = create_engine("mysql+mysqldb://root:" + "password" + "@localhost/ddd", encoding='utf-8')
conn = engine.connect()

# if_exists = "append": 기존 데이터에 추가로 넣음.
final_data.to_sql(name='week_data', con=engine, index=False, if_exists="append")

conn.close()
