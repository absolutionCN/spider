import os
import re
import time
import requests
import json
import random
from queue import Queue
from threading import Thread
from bs4 import BeautifulSoup

url = "https://www.bilibili.com/read/cv3877755"
weizhuang = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"]

headers = {'User-agent': random.choice(weizhuang)}
res = requests.get(url=url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
a = soup.find_all('img')

pic_dict = "./picture/"
if os.path.exists(pic_dict) == False:
    os.mkdir(pic_dict)

file_path = "./下载地址/"
if os.path.exists(file_path) == False:
    os.mkdir(file_path)


def run_time(func):
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        print('running', end - start, 's')

    return wrapper


class Spider():

    def __init__(self):
        self.qurl = Queue()
        self.data = list()
        self.page_num = 50
        self.thread_num = 50

    def xiangao_url(self):
        xiangao_url = "https://search.bilibili.com/article?keyword=%E7%BA%BF%E7%A8%BF&order=attention&category_id0=&page={}"
        for i in range(1, self.page_num + 1):
            url = xiangao_url.format(i)
            res = requests.get(url=url, headers=headers)
            xiangao_soup = BeautifulSoup(res.text, "html.parser")
            a_tag = xiangao_soup.find_all("a", "title")
            for index, href in enumerate(a_tag):
                if href.get('href') == None:
                    pass
                elif "from=search" not in href.get("href"):
                    pass
                else:
                    try:
                        print(href.get('href'))
                        self.qurl.put(href.get('href'))
                    except Exception as e:
                        return e, href.get("href")

    def download_pic(self):
        while not self.qurl.empty():  # 保证url遍历结束后退出线程
            url = self.qurl.get()
            pic_url = "https:" + url
            pic_res = requests.get(url=pic_url, headers=headers)
            pic_soup = BeautifulSoup(pic_res.text, "html.parser")
            pic_name = (pic_soup.find_all('title'))[0].get_text()
            pic_a = pic_soup.find_all('img')
            for index, link in enumerate(pic_a):
                if pic_a:
                    if link.get('data-src') == None:
                        pass
                    else:
                        try:
                            html = requests.get("https:" + link.get('data-src'))
                            img_name = "第{}页第{}张图片".format(pic_name, index + 1)
                            with open(pic_dict + img_name + '.png', "wb") as file:
                                file.write(html.content)
                                file.flush()
                                file.close()
                                print("第{}页第{}张图片下载完成".format(pic_name, index + 1))
                                time.sleep(1)
                        except Exception as e:
                            print(e)
                            pass

    @run_time
    def run(self):
        self.xiangao_url()
        ths = []
        for i in range(self.thread_num):
            th = Thread(target=self.download_pic)
            th.start()
            ths.append(th)

        for th in ths:
            th.join()


#
if __name__ == '__main__':
    Spider().run()

