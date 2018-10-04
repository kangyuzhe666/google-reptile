# encoding: utf-8
'''
@author: gaoyongxian666
@file: google_spider.py
@time: 2018/8/1 14:06
'''
import os
import urllib
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver


# google图片网址
# https://www.google.com/imghp?hl=zh-TW

# browser=webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe")
browser=webdriver.Chrome(executable_path=r"D:/chromedriver.exe")
browser.get('https://www.google.com/imghp?hl=zh-TW')

#lst-ib
inputname = browser.find_element_by_css_selector('#lst-ib')
inputname.send_keys("身份证")

#mKlEF > span > svg
search = browser.find_element_by_css_selector('#mKlEF > span > svg')
search.click()

# 获取当前时间，以时间命名
t = time.localtime(time.time())
foldername = str(t.__getattribute__("tm_year")) + "-" + str(t.__getattribute__("tm_mon")) + "-" + str(
    t.__getattribute__("tm_mday"))  # 定义文件夹的名字
picpath = 'D:\\ImageDownload\\%s' % (foldername)  # 下载到的本地目录
if not os.path.exists(picpath):  # 路径不存在时创建一个
    os.makedirs(picpath)


# 记录下载过的图片地址，避免重复下载
img_url_dic = {}

# 图片命名以数字命名
x = 0

# 当鼠标的位置小于最后的鼠标位置时,循环执行
pos = 0
for i in range(7, 1000):  # 此处可自己设置爬取范围

    pos = i * 1500  # 每次下滚500
    js = "document.documentElement.scrollTop=%d" % pos
    browser.execute_script(js)
    time.sleep(5)

    # 获取页面源码
    html_page = browser.page_source
    # 利用Beautifulsoup4创建soup对象并进行页面解析
    soup = bs(html_page, "lxml")
    # 通过soup对象中的findAll函数图像信息提取
    imglist = soup.findAll('img', {'class': 'rg_ic rg_i'})

    for imgurl in imglist:
        try:
            print(x, end=' ')
            print(imgurl['src'])
            if imgurl['src'] not in img_url_dic:
                target = picpath + '\\%s.jpg' % x
                print ('Downloading image to location: ' + target + '\nurl=' + imgurl['src'])
                f1 = open("url.txt", 'a')
                f1.write(imgurl['src'])
                f1.close()

                img_url_dic[imgurl['src']] = ''
                urllib.request.urlretrieve(imgurl['src'], target)
                time.sleep(0.1)
                x += 1
        except Exception:
            print("ERROR!")
            continue





browser.close()