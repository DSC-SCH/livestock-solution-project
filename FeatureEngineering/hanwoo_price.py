from lxml import etree

import xml.etree.ElementTree as ElementTree
import pandas as pd
import datetime

from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib
import time

import pymysql

# ddd서버에 맞게 변경
db = pymysql.connect(host='localhost', user = 'root', password = '#',db='ddd' )
curs = db.cursor()

# 시간날짜 함수 생성
now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')
print(nowDate)

date = pd.date_range(start=now-datetime.timedelta(days=5), end=now)
date = date.strftime("%Y%m%d").tolist()

# data 수집
for date_ in date:
    # service key 발급받은 후 # 을 변경
    request = urllib.request.Request("http://data.ekape.or.kr/openapi-data/service/user/grade/liveauct?serviceKey=#&auctDate=" +str(date_ ) +"&auctFlag=2")

    time.sleep(0.3)

    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()

    tree = etree.fromstring(response_body)

    for media in tree.getiterator('item'):
        place = media.findtext("abattNm")
        date = media.findtext("auctDate")
        price =media.findtext("hanwooAuctAmt")

    # data db에 저장
    query = "INSERT IGNORE INTO hanwoo_price(date, place, price) VALUES(%s,%s,%s)"
    curs.execute(query,(date,place,price))

# commit 후 닫기
db.commit()
db.close()
