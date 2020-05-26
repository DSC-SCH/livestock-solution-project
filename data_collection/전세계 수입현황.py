from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import pandas

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

path = r'C:\Users\student\Desktop\박성아\chromedriver_win32\chromedriver.exe'

driver = webdriver.Chrome(path)
url = "http://www.kmta.or.kr/kr/data/stats_import_beef_month.php"
driver.get(url)

def divide_list(l, n):
    # 리스트 l의 길이가 n이면 계속 반복
    for i in range(0, len(l), n):
        yield l[i:i + n]


alldf = []

for i in range(10, 23):

    button_path = '/html/body/div[1]/div[5]/form/div/select'

    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, button_path)))

    button.click()

    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[5]/form/div/select/option[" + str(i) + "]")))
    button.click()

    soup = driver.page_source

    target = BeautifulSoup(soup, 'html.parser')

    abc = []
    result = []

    for tag2 in target.find_all('table', class_='table1'):
        for tag in tag2.find_all('td', class_='num_field'):
            abc.append(tag.text)
            # 한 리스트에 몇개씩 담을지 결정
        result = list(divide_list(abc, 3))

        del result[12]

    alldf.extend(result)

import pandas

dt_index = pandas.date_range(start='20070101', end='20191231')
dt_list = dt_index.strftime("%Y%m%d").tolist()

date = pd.DataFrame(dt_list,columns=['date'])
date

date = date.assign(year = date['date'].str.slice(0, 4) )
date = date.assign(month = date['date'].str.slice(4, 6) )

del date['date']
date2 = date.drop_duplicates().reset_index()
del date2['index']

a = pd.DataFrame(alldf,columns=['냉동','냉장','계'])
print(a.shape)
print(date2.shape)

total = pd.concat([date2,a],axis=1)
total

alldf = []

for i in range(7, 10):
    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[5]/form/div/select/option[" + str(i) + "]")))
    button.click()

    soup = driver.page_source

    target = BeautifulSoup(soup, 'html.parser')

    abc = []
    result = []

    for tag2 in target.find_all('table', class_='table1'):
        for tag in tag2.find_all('td', class_='num_field'):
            abc.append(tag.text)
            # 한 리스트에 몇개씩 담을지 결정
        result = list(divide_list(abc, 6))

        del result[12]

    alldf.extend(result)

result

dt_index = pandas.date_range(start='20040101', end='20061231')
dt_list = dt_index.strftime("%Y%m%d").tolist()

date = pd.DataFrame(dt_list,columns=['date'])
date

date = date.assign(year = date['date'].str.slice(0, 4) )
date = date.assign(month = date['date'].str.slice(4, 6) )

del date['date']
date2 = date.drop_duplicates().reset_index()
del date2['index']

a = pd.DataFrame(alldf,columns=['냉동','냉장','계',"냉동금액","냉장금액","금액합계"])
print(a.shape)
print(date2.shape)

total_2004 = pd.concat([date2,a],axis=1)

total_concat = pd.concat([total_2004[["year","month","냉동","냉장","계"]],total])

total_concat.to_csv("전세계 수입현황.csv",encoding='cp949')