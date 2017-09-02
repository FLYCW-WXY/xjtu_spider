# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
url='http://wechat.xanet.edu.cn/attendance.jsp'

#按学号获取考勤刷卡信息
def getXJTUAttendanceData(number):
    try:
        resultList=[]
        r=requests.get(url,{'netid':number},timeout=30)
        r.encoding=r.apparent_encoding
    except:
        return ''
    s=BeautifulSoup(r.text,'html.parser')
    wholeTable=s.find_all('td',{'style':'text-align:center;word-break:break-all;'})
    for i in range(0,len(wholeTable),2):
        resultList.append({'time':wholeTable[i].string,'location':wholeTable[i+1].string})
    return resultList#返回格式[{时间(time),地点(location)}]