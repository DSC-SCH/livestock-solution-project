#!/usr/bin/env python
# coding: utf-8

# In[1]:


from lxml import etree  #xml 파일을 열 때 사용하는 코드
import xml.etree.ElementTree as ElementTree  #xml파일을 여는 코드
import pandas as pd

from urllib.request import urlopen
from urllib.parse import urlencode,unquote,quote_plus
import urllib


# In[3]:


# api주소 열기 (url + 인증키 + 해당페이지+한 화면에 출력되는 데이터 개수)
request = urllib.request.Request('http://apis.data.go.kr/1543000/FarmServiceInfo/getFarmCategoryInfo?serviceKey=70chvGVOwguGdjPrpZL063fX50H6oufjCGWQ77SQ2AL0mOHl9nzn58ipR1dB5G0rjNmt7Xhj%2FZ3pPAXRBOq5Ig%3D%3D&pageNo=1&numOfRows=10&lvstck_code=412000')

request.get_method = lambda: 'GET'
response_body = urlopen(request).read()
# 추출된 xml형식의 text를 xml객체로 파싱
tree = etree.fromstring(response_body)


# In[ ]:


# 빈 벡터 생서
a = []
b = []
c = []
d = []
e = []
f = []
g = []
h = []
i = []

for page in range(1,170):   
    
    # api주소 열기 (url + 인증키 + 해당페이지+한 화면에 출력되는 데이터 개수)
    request = urllib.request.Request('http://apis.data.go.kr/1543000/FarmServiceInfo/getFarmCategoryInfo?serviceKey=70chvGVOwguGdjPrpZL063fX50H6oufjCGWQ77SQ2AL0mOHl9nzn58ipR1dB5G0rjNmt7Xhj%2FZ3pPAXRBOq5Ig%3D%3D&pageNo='
                                     +str(page)+'&numOfRows=1000&lvstck_code=412000')
    
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    
    # 추출된 xml형식의 text를 xml객체로 파싱
    tree = etree.fromstring(response_body)
    
    # 태그로부터 원하는 텍스트 추출
    for media in tree.getiterator('item'):
        a.append(media.findtext('lvstck_nm'))
        b.append(media.findtext('std_farm_no'))
        c.append(media.findtext('farm_nm'))
        d.append(media.findtext('ctprvn_nm')) 
        e.append(media.findtext('sigungu_nm'))
        f.append(media.findtext('brd_head_qy'))
        g.append(media.findtext('owner_se'))   
        h.append(media.findtext('livestock_no'))
        i.append(media.findtext('oper_sttus_nm'))
    


# In[ ]:


df1 = pd.DataFrame(a,columns=['축종'])
df2 = pd.DataFrame(b,columns=['농장번호'])
df3 = pd.DataFrame(c,columns=['농장명'])
df4 = pd.DataFrame(d,columns=['시도명'])
df5 = pd.DataFrame(e,columns=['시군구명'])
df6 = pd.DataFrame(f,columns=['사육두수'])
df7 = pd.DataFrame(g,columns=['소유자구분'])
df8 = pd.DataFrame(h,columns=['축산업허가등록번호'])
df9 = pd.DataFrame(i,columns=['운영상태'])


# In[ ]:


total = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9],axis=1)


# In[ ]:


total.to_csv('가축사육 통계제공 서비스 일부.csv',encoding='utf-8-sig')


# In[ ]:


total.shape


# In[ ]:




