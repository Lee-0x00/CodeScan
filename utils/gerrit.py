# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2018-05-30 16:24:34
# @Author  : Bing (wulitouhaha@vip.qq.com)
# @Link    : ${link}
# @Desc : $Id$

import sys
sys.path.append('..')

import time, re, requests, json, random
from bs4 import BeautifulSoup
from core.settings import *


def Gerrit():
	test_result = []
	project_git_id, project_name, project_description, project_path, created_at, updated_at, project_url, project_contributors, department, project_author  = '', '', '', '', '', '', '', '', '', ''

	url = "{}login/%23%2Fq%2Fstatus%3Aopen".format(gerrit_url)
	_session = requests.Session()
	postData = {'username': '{}'.format(git_user), 'password': '{}'.format(git_pwd)}
	_session.post(url, data = postData)

	url_project = "{}projects/?m=&n=26&type=ALL&d".format(gerrit_url)
	res = _session.get(url_project)
	tt = json.loads(res.text.split(")]}'")[1:][0])
	for k,v in tt.items():
		project_git_id = "gerrit-000-00"
		project_name = k.split("/")[-1]
		project_path = k.__str__()
		project_description = v.get('description').__str__()
		created_at = int(time.time())
		updated_at = int(time.time())
		project_url = "ssh://{}@{}/{}".format(git_user, gerrit_ssh_url , project_path)


		test_result.append((project_git_id, project_name, project_description, project_path, created_at, updated_at, project_url, project_contributors, department, project_author))

		# res = _session.get("{}config/server/info".format(gerrit_url))
		# print(res.text)
	return test_result
