# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2018-05-18 10:58:39
# @Author  : Bing (wulitouhaha@vip.qq.com)
# @Link    : http://example.org
# @Desc : $Id$

import sys
sys.path.append('..')

import time, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from core.settings import *

# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')


# # options = webdriver.ChromeOptions()
# # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# # chrome_driver_binary = r"/mnt/CodeScan/v0.1/thirdparty/chromedriver"
# # driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
# chrome_path = r"/mnt/CodeScan/v0.1/thirdparty/chromedriver"
# driver = webdriver.Chrome(executable_path=chrome_path)

# driver.get("http://www.baidu.com") 
# print(driver.page_source)


t = "2018-04-26T05:27:41.934Z"
tt = t.split(".")[0].replace("T", " ")
dt = time.strptime(tt, "%Y-%m-%d %H:%M:%S")
timestamp = time.mktime(dt)
print(timestamp)

'''

# schedulers = BlockingScheduler()
# schedulers.add_job(SonarMonitor, 'interval', seconds=60, id="sonar-monitor")
# log('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

# try:
# 	schedulers.start()
# except:
# 	schedulers.remove_job("sonar-monitor")

# 多协程执行扫描
# jobs = []
# for i in list(range(0,20)):
# 	jobs.append(gevent.spawn(sonarScan))
# gevent.joinall(jobs)
'''
