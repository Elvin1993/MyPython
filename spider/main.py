#coding=utf-8
from bs4 import BeautifulSoup
import requests

headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mazilla'
    }

url = 'http://www.appchina.com/sou/?keyword=网易云课堂'
web_data = requests.get(url)
soup = BeautifulSoup(web_data.text,'lxml')
title = soup.select('ul > li > div.app-info > h1 > a')[0].get_text()
times = soup.select('ul > li > div.app-info > span.download-count')[0].get_text()
print('在应用汇  ' +title+' 下载量：'+ times)