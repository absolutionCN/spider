# coding=utf-8
# !/usr/bin/python
import requests
import os
import bs4
from bs4 import BeautifulSoup
import sys
import importlib
import json
import random
import urllib
import urllib.request
import time
from fake_useragent import UserAgent

importlib.reload(sys)

# 越多越好
webo_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
    ''
    ''
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
]

global headers
headers = {"User-Agent": random.choice(webo_headers)}

# 定义要爬取微博大V的微博ID
id = "7229718199"

# 设置代理
proxy_addr = "122.241.72.191:808"

# 定义页面打开函数
def use_proxy(url, proxy_addr):
    global headers
    print(headers)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
    return data


# 获取微博主页的containerid，爬取微博内容需要此id
def get_containerid(url):
    data = use_proxy(url, proxy_addr)
    content = json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if (data.get('tab_type') == 'weibo'):
            containerid = data.get('containnerid')
    return containerid

# 获取微博大V账号的用户基本信息，如：微博昵称、微博地址、微博头像、关注人数、粉丝数、性别、等级等
def get_userInfo(id):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
    data = use_proxy(url, proxy_addr)
    content = json.loads(data).get('data')
    user_name = content.get('userInfo').get('screen_name')
    profile_image_url = content.get('userInfo').get('profile_image_url') # 头像地址
    profile_url = content.get('userInfo').get('profile_url') # 微博主页
    followers_count = content.get('userInfo').get('followers_count') # 关注人数
    guanzhu = content.get('userInfo').get('follow_count') # 关注别人人数
    urank = content.get('userInfo').get('urank') # 微博等级
    gender = content.get('userInfo').get('gender') # 性别
    verified = content.get('userInfo').get('verified') # 是否认证
    description = content.get('userInfo').get('description') # 微博说明
    print("微博昵称：" + user_name + "\n" + "微博主页地址：" + profile_url + "\n" + "微博头像地址：" + profile_image_url + "\n" + "是否认证：" + str(
        verified) + "\n" + "微博说明：" + description + "\n" + "关注人数：" + str(guanzhu) + "\n" + "粉丝数：" + str(
        followers_count) + "\n" + "性别：" + gender + "\n" + "微博等级：" + str(urank) + "\n")
    return user_name

# 获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo(id, file):
    i = 1
    while True:
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?containerid=' + get_containerid(
            url) + '&page=' + str(i)
        try:
            data = use_proxy(weibo_url, proxy_addr)
            content = json.loads(data).get('data')
            cards = content.get('cards')
            print('card%s' % cards)
            if (len(cards) > 0 ) :
                for j in range(len(cards)):
                    print('-----正在爬取第' + str(i)) + '页,第' + str(j) + '条微博-----'
                    card_type = cards[j].get('card_type')
                    if card_type == 9 :
                        mblog = card_type[j].get('mblog')
                        created_at = mblog.get('created_at') # 发布时间
                        text = mblog.get('text') # 微博内容
                        reposts_count = mblog.get('reposts_count') # 转发数
                        comments_count = mblog.get('comments_count') # 评论数
                        attitudes_count = mblog.get('attitudes_count') # 点赞数
                        scheme = mblog.get('scheme') # 微博地址
                        pictures = mblog.get('pics')  # 正文配图，返回list
                        pic_urls = [] # 存储图片url地址
                        if pictures:
                            for picture in pictures:
                                pic_url = picture.get('large').get('url')
                                pic_urls.append(pic_url)

                        # 保存文本
                        with open(file, 'a', encoding='utf-8') as fh:
                            if len(str(created_at)) < 6:
                                