# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2018-05-30 16:24:34
# @Author  : Bing (wulitouhaha@vip.qq.com)
# @Link    : ${link}
# @Desc : $Id$

import sys
sys.path.append('..')

import time, re, requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from core.settings import *

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')


def Gerrit():
	test_result = []
	project_git_id, project_name, project_description, project_path, created_at, updated_at, project_url, project_contributors, department, project_author  = '', '', '', '', '', '', '', '', '', ''

	# 登陆
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=os.path.join(BASEDIR, "thirdparty/chromedriver") )
	driver.get(gerrit_url + "login/") 
	time.sleep(5)
	driver.find_element_by_name("username").send_keys("{}".format(git_user))
	driver.find_element_by_name("password").send_keys("{}".format(git_pwd))


	all_input = driver.find_elements_by_tag_name("input")
	for i in all_input:
		value = i.get_attribute("value").__str__().strip()
		if "Sign In" == value :
			i.click()

	# 获取项目名称和描述
	html_table = ""
	driver.get(gerrit_url + "#/admin/projects/")
	time.sleep(5)
	html = BeautifulSoup(driver.page_source, "html5lib")
	# html = BeautifulSoup(driver.page_source, "lxml")
	for i in html.find_all("table"):
		value = i.attrs.get('class')
		if value:
			tag = value[0].__str__()
			if tag == "changeTable" :
				html_table = i
				break

	for i in html_table.find_all("tr")[1:]:
		for j in i.find_all("td"):
			for k in j.find_all("a"):
				tt = r"#\/admin\/projects\/"
				link = k["href"]
				matchObj = re.match(tt, link, re.M|re.I)
				if matchObj:
					project_git_id = "gerrit-000-00"
					project_name = link.split("/")[-1]
					project_path = link 
					created_at = int(time.time())
					updated_at = int(time.time())

					test = gerrit_url + link
					driver.get(test)
					time.sleep(5)
					project_url = driver.find_element_by_class_name("com-google-gwtexpui-clippy-client-ClippyCss-label").text

					test2 = gerrit_url + link + ",access"
					driver.get(test2)
					html = BeautifulSoup(driver.page_source, "html5lib")
					for l in html.find_all("a", class_="com-google-gerrit-client-admin-PermissionRuleEditor_BinderImpl_GenCss_style-groupName") :
						department = l.text

					test_result.append((project_git_id, project_name, project_description, project_path, created_at, updated_at, project_url, project_contributors, department, project_author))

	# 关闭所有窗口
	driver.quit()
	return test_result


# print(Gerrit())


'''
# from selenium import webdriver
# import dns.resolver

# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-setuid-sandbox")

# 使用splinter 模拟浏览器
# browser = Browser("phantomjs")
# browser.visit("/login/")
# print(driver.status_code,driver.url,driver.title)

# # 使用selenium 模拟浏览器
# browser = webdriver.Chrome()
# browser.get('http://www.baidu.com/')

# .find_element_by_class_name("changeTable")
# project_table = tt.find_elements_by_tag_name("tr")
# for i in project_table:
# 	print("sd")
# 	project_column = i.find_elements_by_tag_name("td")
# 	for j in project_column:
# 		print(j.get_attribute("class"))



# driver.get_screenshot_as_file("baidu_img2.jpg")
# , i.get_attribute(), i.get_property(), i.size()

# myAttrs={‘class‘:‘footer‘}	 bs.find_all(name=‘div‘,attrs=myAttrs)
#1.soup.find_all("a", class_="sister")
#2.css_soup.find_all("p", class_="body")
#3.soup.find_all(href=re.compile("elsie"))
driver.title, driver.get_cookies()
'''
