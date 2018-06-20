# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2018-05-18 10:58:39
# @Author  : Bing (wulitouhaha@vip.qq.com)
# @Link    : http://example.org
# @Desc : $Id$

import sys
sys.path.append('..')

import os, shutil, requests, json, time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from core.settings import ding_Token


def getFileName(path, list_name):  
	# 列出目录下所有文件名
	for file in os.listdir(path):  
		file_path = os.path.join(path, file)  
		if os.path.isdir(file_path):  
			getFileName(file_path, list_name)  
		else:  
			list_name.append(file)
	return list_name


def makeDir(path):
	# 创建目录
	os.makedirs(path)
	return True


def delDir(path):
	# 删除目录下所有文件
	try:
		delList = os.listdir(path)
		for f in delList:
			filePath = os.path.join(path,f)
			if os.path.isfile(filePath):
				os.remove(filePath)
			elif os.path.isdir(filePath):
				shutil.rmtree(filePath,True)
		return True
	except:
		return True


def getFileSuffix(path):
	# 获取项目目录下所有文件名
	allfile = []
	result_content = getFileName(path, allfile)

	# 获取出现次数最多的文件后缀名
	prefix = ['java', 'py', 'c', 'php', 'js', 'c', 'jsp', 'xml']
	result = {"java" : 0, "py" : 0, "c" : 0, "php" : 0, "js" : 0, "c" : 0, "jsp" : 0, "xml" : 0}
	for i in result_content:
		try:
			suffix = i.split('.')[-1]
			if suffix in prefix:
				result[str(suffix)] += 1
		except:
			pass

	return sorted(result, key = lambda x:result[x])[-1]


def dingNotify(text):
	# 钉钉提醒
	try:
		msg = {
			"title":"自动化代码检测",
			"text": "{}".format(text)
		}
		url  = "https://oapi.dingtalk.com/robot/send?access_token={}".format(ding_Token);
		data = json.dumps({'msgtype':'markdown','markdown':msg});
		headers = {'Content-Length': "%s" % len(data),'content-type': 'application/json'}
		r = requests.post(url = url , data = data, headers = headers, verify= False)
	except:
		pass
	return True


def gitlab_time_switch(strings):
	tt = strings.split(".")[0].replace("T", " ")
	dt = time.strptime(tt, "%Y-%m-%d %H:%M:%S")
	timestamp = int(time.mktime(dt))
	return timestamp

