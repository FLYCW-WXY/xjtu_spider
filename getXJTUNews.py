# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import bs4
edunewsbaseurl='http://due.xjtu.edu.cn/jxxx/xytz/'#教学信息 学业通知的基础地址
libnewsurl='http://mc.m.5read.com/weixin/customize_showList.jspx?schoolId=63&protocol=31'#图书馆新闻地址
activitiesurl='http://oa.xjtu.edu.cn/form/user/anonymous/dxhd_index.jsp'#校园大型活动的地址

def getHTMLContent(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""

#获取教务新闻
def getXJTUEduNews(type):#'xjgl':'学籍管理','ksap':'考试安排','kcap':'课程安排','xjjl':'校际交流','jsap':'竞赛安排','zyfx':'专业辅修','dcxm':'大创项目'
    resultList=[]
    if type=='':
        s = BeautifulSoup(getHTMLContent('http://due.xjtu.edu.cn/jxxx/xytz.htm'),
                          'html.parser')
        for div in s.find_all('div', {'class': 'list-li'}):
            resultList.append({'date': div('span')[0].string, 'title': div('a')[0].attrs['title'],
                               'link': 'http://due.xjtu.edu.cn' + div('a')[0].attrs['href'][2:]})
        return resultList  #返回格式[{日期(date),新闻标题(title),链接(link)}]
    s=BeautifulSoup(getHTMLContent(edunewsbaseurl+type+'.htm'),'html.parser')
    for div in s.find_all('div',{'class':'list-li'}):
        resultList.append({'date':div('span')[0].string,'title':div('a')[0].attrs['title'],'link':'http://due.xjtu.edu.cn'+div('a')[0].attrs['href'][5:]})
    return resultList#返回格式[{日期(date),新闻标题(title),链接(link)}]

#获取图书馆公告
def getXJTULibNews():
    resultList=[]
    s=BeautifulSoup(getHTMLContent(libnewsurl),'html.parser')
    for li in s.find_all('li'):
        resultList.append({'date':li('em')[0].string,'title':li('p',{'class':'title'})[0].string,'link':li('a')[0].attrs['href']})
    return resultList#返回格式[{日期(date),新闻标题(title),链接(link)}]

#获取校园活动
def getXJTUCampAct():
    resultList=[]
    s=BeautifulSoup(getHTMLContent(activitiesurl),'html.parser')#学籍管理、考试安排、课程安排、校际交流、竞赛安排、专业辅修、大创项目
    for tr in s.find_all('tr',{'id':'test'}):
        item=tr('td')
        resultList.append({'title':item[0].string,'time':item[1].string,'location':item[2].string,'host':item[3].string})
    return resultList[1:]#返回格式[{活动名称(title),活动时间(time),活动地点(location),主办承办单位(host)}]