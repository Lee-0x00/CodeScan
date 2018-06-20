# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2018-05-18 10:58:39
# @Author  : Bing (wulitouhaha@vip.qq.com)
# @Link    : http://example.org
# @Desc : $Id$

import sys
sys.path.append('..')

import requests, os
import collections
from lib.common import delDir, getFileSuffix, gitlab_time_switch
from utils.excute import pull
from core.settings import  * #git_token, git_api,

class GitLAB(object):
	def __init__(self):
		self.headers = git_token


	def getAllProjects(self):
		try:
			url = "{}oauth/token".format(ding_URL)
			res = requests.post(url, data= ding_Data, timeout=3)
			access_token = res.json()["access_token"]
			http_header = {
				"Accept" : "application/json",
				"Authorization" : "Bearer %s" % access_token
			}
		except:
			pass

		try:
			url = git_api + "projects?per_page=200"
			result = requests.get(url, headers = self.headers, verify = False)
			data = result.json()
			tt = []
			for row in data:
			# for row in data[1:10]:
				project_git_id, project_name, project_description, project_path, created_at, updated_at, project_url, project_contributors, department, project_author  = '', '', '', '', '', '', '', '', '', ''
				# 获取项目基础信息
				try:
					project_author = row["owner"]["name"]
				except:
					project_author = ""
				project_url = row["http_url_to_repo"]
				project_git_id = row["id"]
				project_name = row["name"]
				project_description = row["description"]
				project_path = row["name_with_namespace"]
				created_at = gitlab_time_switch(row["namespace"]["created_at"])
				updated_at = gitlab_time_switch(row["last_activity_at"])
				project_contributors = self.getContributors(int(project_git_id))
				result = []
				for username in project_contributors:
					customer_username = username.__str__().split("@")[0]
					try:
						url = "{}api/info/user/{}".format(ding_URL, customer_username)
						res = requests.get(url, headers=http_header, timeout=3)
						department_id = res.json()["data"]["department_id"]
						if department_id:
							url = "{}api/info/departments/{}".format(ding_URL, department_id)
							res = requests.get(url, headers=http_header)
							department_name = res.json()["data"]["fullname"]
							result.append(department_name) 
					except Exception as e:
						pass

				try:
					data = collections.Counter(result)
					department = sorted(data,key = lambda x:data[x])[-1]
				except:
					department = ""
				project_contributors = ",".join(project_contributors)
				tt.append((project_git_id, project_name, project_description, project_path, created_at, updated_at, project_url, project_contributors, department, project_author))
			return tt
		except Exception as e:
			# print(e)
			return False


	def getProjects(self, id):
		try:
			url = git_api + "projects"
			result = requests.get(url, headers = self.headers, verify = False)
			data = result.json()
			for row in data:
				if int(row["id"]) == int(id):
					result = {
						"id" : row["id"], 
						"description" : row["description"], 
						"name_with_namespace" : row["name_with_namespace"], 
						"name" : row["name"], 
						"author" : row["author"],
						"created_at" : row["namespace"]["created_at"], 
						"updated_at" : row["last_activity_at"]
					}
					return result
		except Exception as e:
			return False


	def getContributors(self, id):
		try:
			# url = git_api + "projects/%s/users" % id
			url = git_api + "projects/%s/repository/contributors" % id
			result = requests.get(url, headers = self.headers, verify = False)
			data = result.json()
			result = []
			for row in data:
				test = row["email"].__str__().strip('“')
				test = test.strip('”')
				# test = row['username']
				result.append(test)
			return result
		except Exception as e:
			return []


'''
def getLanguages(self, id):
	url = git_api + "projects/%s/languages" % id
	url2 = git_api + "projects/201/repository/commits"
	result = requests.get(url2, headers = self.headers, verify = False)
	data = result.json()
	print(data)
	# language = sorted(data,key = lambda x:data[x])[-1]
	# return language

#https://git.ynpay.cc/api/v3/projects/all?per_page=100&page=1?private_token=XXXXXX，其实用http也可以。
'''



