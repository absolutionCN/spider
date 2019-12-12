from bs4 import BeautifulSoup
import urllib.request
from urllib import error

test_url = "https://www.baidu.com/"  # 测试ip是否可用
proxy_url = "http://www.xicidaili.com/nn/1"  # ip抓取源
ip_file = "availableIP.txt"


# 把ip写入到文件中
def write_file(available_list):
    try:
        with open(ip_file, "w+") as f:
            for available_ip in available_list:
                f.write(available_ip + "\n")
    except OSError as reason:
        print(str(reason))


# 检测代理ip是否可用，返回可用代理ip列表
def test_ip(test_list):
    available_ip_list = []
    for test in test_list:
        proxy = {'http': test}
        try:
            handler = urllib.request.ProxyHandler(proxy)
            opener = urllib.request.build_opener(handler)
            urllib.request.install_opener(opener)
            test_resp = urllib.request.urlopen(test_url)
            if test_resp.getcode() == 200:
                available_ip_list.append(test)
        except error.HTTPError as reason:
            print(str(reason))
    return available_ip_list


# 抓取西刺代理ip
def catch_ip():
    ip_list = []
    try:
        # 要设置请求头，不然503
        headers = {
            'Host': 'www.xicidaili.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        req = urllib.request.Request(proxy_url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=20)
        content = resp.read()
        soup = BeautifulSoup(content, 'html.parser')
        catch_list = soup.find_all('tr')[1:]

        # 保存代理ip
        for i in catch_list:
            td = i.find_all('td')
            ip_list.append(td[1].get_text() + ":" + td[2].get_text())

        return ip_list
    except urllib.error.URLError as reason:
        print(str(reason))


if __name__ == "__main__":
    xici_ip_list = catch_ip()
    available_ip_list = test_ip(xici_ip_list)
    write_file(available_ip_list)

