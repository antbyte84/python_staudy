#!/usr/bin/env python

from bs4 import BeautifulSoup
from urllib.request import urlopen
import os, urllib,string
import socket
from urllib import request
from urllib import response
from urllib import parse
import time
import http

def paserUrl(file, urlPath, parsedUrl):
    print(urlPath)
    #file.writelines(urlPath+ '\n')
    #将链接中的中文转为可用字符
    urlPath = urllib.parse.quote(urlPath, safe=string.printable)
    # set up authentication info
    #authinfo = urllib.request.HTTPBasicAuthHandler()
    #authinfo.add_password(realm='PDQ Application', uri=urlPath, user=user, passwd=passwd)
    # 代理开关，表示是否启用代理
    proxyswitch = True
    httpproxy_handler = urllib.request.ProxyHandler({"http" : "http://proxy.xxx.com.cn:8080"})
    nullproxy_handler = urllib.request.ProxyHandler({})
    # build a new opener that adds authentication and caching FTP handlers
    if proxyswitch:
        opener = urllib.request.build_opener(httpproxy_handler, urllib.request.CacheFTPHandler)
    else:
        opener = urllib.request.build_opener(nullproxy_handler, urllib.request.CacheFTPHandler)
    # 构建一个全局opener，之后所有的请求都可以用urlopen（）方式发出去，也附带handler功能
    #urllib.request.install_opener(opener)
    request_headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "cache-control":"max-age=0",
    "sec-fetch-mode":"navigate",
    "sec-fetch-site":"none",
    "sec-fetch-user":"?1",
    "upgrade-insecure-requests":"1"
    }
    request_headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    }
    req = request.Request(urlPath, headers=request_headers)
    html_content = None
    childList = []
    try:
        html = request.urlopen(req, timeout=10)
    except Exception as e:
        print('URL error occur'+str(e))
        return childList
    try:
        html = html.read()
    except http.client.IncompleteRead as e:
        print('http client incompleteRead' + str(e))
        return childList
    #print(html)
    soup = BeautifulSoup(html, "html.parser")
    if soup.body == None:
        return childList
    #整理a标签中数据
    all_content = soup.body.find_all('a')
    if all_content != None:
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
                if childList.count(path) == 0 and path.startswith('http'):
                    if path not in parsedUrl:
                        childList.append(path)
    #整理p标签中数据
    all_txt = soup.body.find_all('p')
    if all_txt != None:
        for child in all_txt:
            if child.string and child.string != '\n' and child.string != ' ':
                txt = child.string.strip()
                print(txt)
                file.writelines(txt+ '\n')
    file.writelines('\n')
    #return childList
    return list(set(childList))

def pachong(file, urlPath):
    parsedUrl = []
    parsedUrl += urlPath
    childList = paserUrl(file, urlPath, parsedUrl)
    time.sleep(10)
    listCount = len(childList)
    i = 0
    tmpList = []
    print('parse child')
    print(listCount)
    #避免使用递归扫描,使用层级扫描
    while i < listCount:
        child  = childList[i]
        parsedUrl += child
        urlList = paserUrl(file, child, parsedUrl)
        tmpList += urlList
        print(len(urlList))
        print(len(tmpList))
        time.sleep(10)
        i += 1
        if i == listCount:
            #childList = tmpList.copy()
            childList = list(set(tmpList.copy()))
            tmpList.clear()
            i = 0
            listCount = len(childList)
            print('parse children\'s child')
            print(listCount)

if __name__ == '__main__':
    basedir = '.'
    targetFile = basedir + '/' + 'pachong.txt'
    f = open(targetFile, 'w', encoding='utf-8')
    urlPath = 'https://www.taobao.com/'
    pachong(f, urlPath)
    f.close()