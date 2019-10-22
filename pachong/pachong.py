#!/usr/bin/env python

from bs4 import BeautifulSoup
from urllib.request import urlopen
import os, urllib,string
import socket
from urllib import request
from urllib import response
from urllib import parse
import time

def paserUrl(file, urlPath):
    print(urlPath)
    #file.writelines(urlPath+ '\n')
    request_headers={
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) Firefox/59.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    }
    #将链接中的中文转为可用字符
    urlPath = urllib.parse.quote(urlPath, safe=string.printable)
    req = request.Request(urlPath, headers=request_headers)
    html_content = None
    childList = []
    try:
        html = request.urlopen(req, timeout=10)
    except Exception as e:
        print('URL error occur'+str(e))
        return childList
    html = html.read()
    #print(html)
    soup = BeautifulSoup(html, "html.parser")
    #整理a标签中数据
    all_content = soup.body.find_all('a')
    for child in all_content:
        #print(child.attrs)
        #a标签中属性
        if child.string and child.string != '\n' and child.string != ' ':
            txt = child.string.strip()
            print(txt)
            file.writelines(txt+ '\n')
        urlList = list(child.attrs.keys())
        #a标签中title内容
        if urlList.count("title") != 0:
            title =  child.attrs["title"]
            print(title)
            file.writelines(title+ '\n')
        #a标签中cuntitle内容
        if urlList.count("cntitle") != 0:
            cntitle =  child.attrs["cntitle"]
            print(cntitle)
            file.writelines(cntitle+ '\n')
        #获取标签中子网页链接
        if urlList.count("href") != 0:
            path = child.attrs["href"]
            if childList.count(path) == 0 and path.find('http') != -1:
                childList.append(path)
    #整理p标签中数据
    all_txt = soup.body.find_all('p')
    for child in all_txt:
        if child.string and child.string != '\n' and child.string != ' ':
            txt = child.string.strip()
            print(txt)
            file.writelines(txt+ '\n')
    file.writelines('\n')
    return childList

def pachong(file, urlPath):
    childList = paserUrl(file, urlPath)
    time.sleep(60)
    listCount = len(childList)
    i = 0
    tmpList = []
    print('parse child')
    print(listCount)
    #避免使用递归扫描,使用层级扫描
    while i < listCount:
        child  = childList[i]
        urlList = paserUrl(file, child)
        tmpList += urlList
        print(len(urlList))
        print(len(tmpList))
        time.sleep(60)
        i += 1
        if i == listCount:
            childList = tmpList.copy()
            tmpList.clear()
            i = 0
            listCount = len(childList)
            print('parse children\'s child')
            print(listCount)

if __name__ == '__main__':
    basedir = '.'
    targetFile = basedir + '/' + 'pachong.txt'
    f = open(targetFile, 'w', encoding='utf-8')
    urlPath = 'https://www.taobao.com'
    pachong(f, urlPath)
    f.close()