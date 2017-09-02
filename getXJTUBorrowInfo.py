# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import datetime
url='http://202.117.24.31/sms/opac/user/lendStatus.action'
def getXJTUBorrowInfo(code):#身份识别码
    resultList=[]
    r=requests.get(url,{'xc':3,'sn':code},timeout=30)
    r.encoding=r.apparent_encoding
    s=BeautifulSoup(r.text,'html.parser')
    for div in s.find_all('div',{'class':'sheet'}):
        name=div('th',{'class':"sheetHd"})[0].get_text().strip()
        deadline=datetime.datetime.strptime(div('td',text=re.compile('到期'))[0].string,'到期 %y-%m-%d')
        resultList.append({'name':name, 'deadline':deadline})
    return resultList#返回格式[{书名(name),到期时间(deadline)}]