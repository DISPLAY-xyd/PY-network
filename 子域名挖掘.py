#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/4 14:53
# @Author  : Display
# @File    : 子域名挖掘.py
# @Software: PyCharm
import requests
import re
from urllib.parse import urlencode
import threading
#查询子域名
def scan_domain(domain,page):
    sub_domains = []
    url = "https://www.baidu.com/s?wd=site:%s&pn=%d"%(domain,page*10)
    print(url)
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    }
    resp = requests.get(url,headers=headers)
    html_str = resp.text
    #数据解析
    pattern = re.compile('class="c-showurl c-color-gray".*?>(.*?)<')
    results = re.findall(pattern,html_str)
    for res in results:
        if "." in res:
            if "/" in res:
                sub_d = res.split('/')[0]
                sub_domains.append(sub_d)
    print(sub_domains)
    return sub_domains

if __name__ == "__main__":
    domain = input("Input scan domain:")
    pages = int(input("input scrapy page:"))
    # sub_domains = scan_domain(domain,pages)
    threads = []
    for page in range(pages):
        t = threading.Thread(target=scan_domain,args=(domain,page))
        threads.append(t)
    for t in threads:
        t.start()
