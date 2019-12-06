import requests
import json
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

headers = {'user-agent':UserAgent().random}







def proxy_list():
    ip_list = []
    try:
        proxy_url = 'https://www.xicidaili.com/nn'
        response = requests.get(proxy_url, headers=headers)
        html = response.content
        proxy_soup = BeautifulSoup(html, 'html.parser')
        proxyList = proxy_soup.find_all('tr')[1:]
        for i in proxyList:
            td = i.find_all('td')
            ip_list.append(td[1].get_text() + ":" + td[2].get_text())
        return ip_list
    except requests.HTTPError as reason:
        print(str(reason))




proxy_list()