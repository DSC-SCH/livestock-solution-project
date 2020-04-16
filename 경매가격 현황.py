#!/usr/bin/env python
# coding: utf-8

# In[8]:


from lxml import etree
import xml.etree.ElementTree as ElementTree
import pandas as pd

from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib

import time


# In[3]:


request = urllib.request.Request("http://data.ekape.or.kr/openapi-data/service/user/grade/liveauct?serviceKey=70chvGVOwguGdjPrpZL063fX50H6oufjCGWQ77SQ2AL0mOHl9nzn58ipR1dB5G0rjNmt7Xhj%2FZ3pPAXRBOq5Ig%3D%3D&auctDate=20030101&auctFlag=2")


# auctFlag = 2 [지육상장제외]   
# auctFlag = 3 [지육상장]

# In[4]:


request.get_method = lambda: 'GET'
response_body = urlopen(request).read()
tree = etree.fromstring(response_body)


# In[14]:


# 시간날짜 함수 생성 
date = pd.date_range(start='20030101', end='20191231')
date = date.strftime("%Y%m%d").tolist()


# In[15]:


date


# In[16]:


a = []
b = []
c = []
d = []
e = []
f = []
g = []
h = []
i = []

for date_ in date:
    request = urllib.request.Request("http://data.ekape.or.kr/openapi-data/service/user/grade/liveauct?serviceKey=70chvGVOwguGdjPrpZL063fX50H6oufjCGWQ77SQ2AL0mOHl9nzn58ipR1dB5G0rjNmt7Xhj%2FZ3pPAXRBOq5Ig%3D%3D&auctDate="+str(date_)+"&auctFlag=2")
    
    time.sleep(0.3)
    
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
        
    tree = etree.fromstring(response_body)
    
    for media in tree.getiterator('item'):
        a.append(media.findtext("abattCode"))
        b.append(media.findtext("abattNm"))
        c.append(media.findtext("auctDate"))
        d.append(media.findtext("hanwooAuctAmt"))
        e.append(media.findtext("hanwooAuctCnt"))
        f.append(media.findtext("hanwooAuct_0bAmt"))
        g.append(media.findtext("hanwooAuct_4bAmt"))
        h.append(media.findtext("hanwooAuctdiffAmt"))
        i.append(media.findtext("hanwooAuctexpectCnt"))


# In[17]:


df1 = pd.DataFrame(a,columns=['작업장코드'])
df2 = pd.DataFrame(b,columns=['도매시장명'])
df3 = pd.DataFrame(c,columns=['경매일자'])
df4 = pd.DataFrame(d,columns=['한우 평균경매 금액'])
df5 = pd.DataFrame(e,columns=['한우 경매 예상 두수'])
df6 = pd.DataFrame(f,columns=['한우 1B+ 경매단가'])
df7 = pd.DataFrame(g,columns=['한우 3B 경매단가'])
df8 = pd.DataFrame(h,columns=['한우 평균경매 금액'])
df9 = pd.DataFrame(i,columns=['한우 경매 낙찰 두수'])


# In[18]:


total = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9],axis=1)

total.to_csv('경매가격현황_지육상장제외.csv',encoding='utf-8-sig')


# In[19]:


total.to_pickle('경매가격현황_지육상장제외.pkl')


# In[20]:


a = []
b = []
c = []
d = []
e = []
f = []
g = []
h = []
i = []

for date_ in date:
    request = urllib.request.Request("http://data.ekape.or.kr/openapi-data/service/user/grade/liveauct?serviceKey=70chvGVOwguGdjPrpZL063fX50H6oufjCGWQ77SQ2AL0mOHl9nzn58ipR1dB5G0rjNmt7Xhj%2FZ3pPAXRBOq5Ig%3D%3D&auctDate="+str(date_)+"&auctFlag=3")
    
    time.sleep(0.3)
    
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
        
    tree = etree.fromstring(response_body)
    
    for media in tree.getiterator('item'):
        a.append(media.findtext("abattCode"))
        b.append(media.findtext("abattNm"))
        c.append(media.findtext("auctDate"))
        d.append(media.findtext("hanwooAuctAmt"))
        e.append(media.findtext("hanwooAuctCnt"))
        f.append(media.findtext("hanwooAuct_0bAmt"))
        g.append(media.findtext("hanwooAuct_4bAmt"))
        h.append(media.findtext("hanwooAuctdiffAmt"))
        i.append(media.findtext("hanwooAuctexpectCnt"))


# In[21]:


df1 = pd.DataFrame(a,columns=['작업장코드'])
df2 = pd.DataFrame(b,columns=['도매시장명'])
df3 = pd.DataFrame(c,columns=['경매일자'])
df4 = pd.DataFrame(d,columns=['한우 평균경매 금액'])
df5 = pd.DataFrame(e,columns=['한우 경매 예상 두수'])
df6 = pd.DataFrame(f,columns=['한우 1B+ 경매단가'])
df7 = pd.DataFrame(g,columns=['한우 3B 경매단가'])
df8 = pd.DataFrame(h,columns=['한우 평균경매 금액'])
df9 = pd.DataFrame(i,columns=['한우 경매 낙찰 두수'])


# In[22]:


total = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9],axis=1)

total.to_csv('경매가격현황_지육상장.csv',encoding='utf-8-sig')
total.to_pickle('경매가격현황_지육상장.pkl')


# In[ ]:




