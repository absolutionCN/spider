#coding=utf-8
'''
author=WLT
createTime=DEC 06 19
'''

import json
import requests
import os
import urllib.request
import urllib.parse
from urllib import error
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

novel_url = 'https://www.biqukan.com/2_2972/'  # 小说页面
base_url = "http://www.biqukan.com"  # 根地址
# 定义存储位置
global save_path
save_path = 'E:/spider/小说爬虫/裁决/'

global headers
headers = {"user-agent": UserAgent().random}


# 创建文件夹
def createDir(save_path):
    if os.path.exists(save_path) is False:
        os.makedirs(save_path)
    # 切换路径至上面创建的文件夹
    # os.chdir(save_path)
    return save_path


# 保存小说到本地
def save_chapter(txt, save_path):
    try:
        with open(save_path, 'a+', encoding='utf-8') as f:
            f.write(txt.get_text(strip=True))
    except (error.HTTPError, OSError) as reason:
        print(str(reason))
    else:
        print('下载完成' + save_path)


# 获取章节链接,和章节名称
def getChapterLinkName():
    global headers
    response = requests.get(novel_url, headers=headers)
    html = response.content
    # 把网页进行编码
    chapter_soup = BeautifulSoup(html, 'html.parser')
    # 选择章节部分
    listmain = chapter_soup.find_all(attrs={'class': 'listmain'})
    # 存放a标签
    a_list = []
    # 提取a标签
    for i in listmain:
        if 'a' not in str(i):
            continue
        for d in i.findAll('a'):
            a_list.append(d)
    result_list = a_list[12:]
    return result_list


# 获取章节内容下载
def getChapterContent(chapter):
    chapter_url = base_url + chapter.get('href')  # 获取url
    chapter_name = chapter.string  # 获取章节名称
    response = requests.get(chapter_url)
    html = response.content
    chapter_content = BeautifulSoup(html, 'html.parser')
    # 查找章节内容
    chapter_text = chapter_content.find_all(attrs={'class': 'showtxt'})
    for txt in chapter_text:
        save_chapter(txt, save_path + chapter_name + '.txt')


if __name__ == '__main__':
    createDir(save_path)
    novel_list = getChapterLinkName()
    for chapter in novel_list:
        getChapterContent(chapter)
