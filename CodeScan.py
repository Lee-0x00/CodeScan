# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2018-05-18 10:58:39
# @Author  : Bing (wulitouhaha@vip.qq.com)
# @Link    : http://example.org
# @Desc : 代码安全审计v0.1--实时监控-多线程

import os, time, requests, json
from collections import Counter
from core.settings import ding_URL, ding_Data
from lib.common import *
from lib.database import *
from lib.logger import log
from utils.gitlab import GitLAB
from utils.gerrit import Gerrit
from utils.excute import scan, pull

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

DBS = Database()


def insertBug(row):
	project_git_id, project_name, project_description, project_path, created_at, updated_at, project_url,project_contributors, department, project_author  = row
	git_project_dir = os.path.join(SONAR_SCAN_DIR, project_name)

	notify_success_data = []
	notify_fail_data = []
	# 查询漏洞信息
	project_sonar_id, bug_id, bug_name, bug_type, bug_severity, bug_fix_status, bug_ctime, bug_ftime, linkid = '', '', '', '', '', '', '', '', ''
	try:
		sql = "select name,project_uuid from projects where qualifier='TRK' and name=%s;"
		sonar_data = DBS.sonar_selectone(sql, (project_name))
		project_name, project_sonar_id = sonar_data
	except:
		if str(project_name) == "All-Projects" :
			pass
		else:
			dingNotify("#### 代码安全审计v0.1\n\n###### {}项目: 未扫描成功 ...".format(project_name))
		return True

	linkid = sonar_url + '/dashboard?id={}'.format(project_name)
	sql = "select issues.id, rules.name, rules.rule_type, issues.severity, issues.resolution, issues.created_at from issues,rules where project_uuid=%s and rules.id = issues.rule_id;"
	scan_bug_data = DBS.sonar_select(sql, (project_sonar_id,))
	for j in scan_bug_data:
		bug_id, bug_name, bug_type, bug_severity, bug_fix_status, bug_ctime = j
		# bug_type: 1 坏味道 2 Bugs 3 漏洞
		if str(bug_type) == '2' or str(bug_type) == '3' :
			sql = "select count(*) from sonar_codebug where bug_id=%s;"
			soc_bug_data = DBS.soc_selectone(sql,(bug_id,))
			count = soc_bug_data[0]
			# 根据bug_id，判断漏洞是否重复
			if count == 0 :
				sql = "insert into sonar_codebug(id, project_name, project_sonar_id, bug_id, bug_name, bug_type, bug_severity, bug_fix_status, bug_ctime, bug_ftime, linkid) value(0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				result = DBS.soc_excute(sql, (project_name, project_sonar_id, bug_id, bug_name, bug_type, bug_severity, bug_fix_status, bug_ctime, bug_ftime, linkid ))
				if result:
					notify_success_data.append(bug_name)
				else:
					notify_fail_data.append(bug_name)
			else:
				bug_ftime = int(time.time())
				sql = "update sonar_codebug set bug_fix_status=%s,bug_ftime=%s where bug_id=%s;"
				result = DBS.soc_excute(sql,(bug_fix_status, bug_ftime, bug_id))
				if result:
					notify_success_data.append(bug_name)
				else:
					notify_fail_data.append(bug_name)

	if len(notify_success_data) > 0:
		dingNotify("#### 代码安全审计v0.1\n\n###### {}项目: 新增{}个bug, 写入失败{}个bug".format(project_name , len(notify_success_data), len(notify_fail_data)))

	# 删除目录项目信息
	delDir(git_project_dir)
	return True


def sonarScan(row):
	result = ""
	project_git_id, project_name, project_description, project_path, created_at, updated_at, project_url,project_contributors, department, project_author  = row
	# 创建临时sonar扫描主目录
	git_project_dir = os.path.join(SONAR_SCAN_DIR, project_name)
	isExists = os.path.exists(SONAR_SCAN_DIR)
	if isExists :
		if os.path.exists(git_project_dir):
			delDir(git_project_dir)
	else:
		makeDir(SONAR_SCAN_DIR)

	# 执行拉取
	pull(project_git_id, project_url, SONAR_SCAN_DIR)
	# 执行扫描
	result = scan(project_git_id, project_name, git_project_dir)
	return result


def run(projectsByGit):
	sonar_result = ""
	result = []

	# 遍历项目信息
	for row in projectsByGit:
		project_git_id, project_name, project_description, project_path, created_at, updated_at, project_url, project_contributors, department, project_author = row

		# 判断项目是否存在
		sql = "select count(*) from sonar_project where project_path=%s;"
		data = DBS.soc_select(sql, project_path)[0][0]
		row = (project_git_id, project_name, project_description, project_path, created_at, updated_at, project_url,project_contributors, department, project_author)
		# print(data)
		if int(data) == 1:
			# 判断项目是否更新
			try:
				sql = "select updated_at from sonar_project where project_path=%s;"
				data = DBS.soc_select(sql, project_path)[0][0]
				if str(data) != str(updated_at):
					if sonarScan(row) :
						if project_git_id == "gerrit-000-00":
							sql = "update sonar_project set project_contributors=%s, updated_at=%s, project_author=%s where project_path=%s;"
							tt = DBS.soc_excute(sql, (project_contributors, updated_at, project_author, project_path))
						else:
							sql = "update sonar_project set project_contributors=%s, updated_at=%s, project_author=%s where project_git_id=%s;"
							tt = DBS.soc_excute(sql, (project_contributors, updated_at, project_author, project_git_id))

						if tt:
							log( " {}项目:已更新 ".format(project_name) )
							insertBug(row)
						else:
							dingNotify("#### 代码安全审计v0.1\n\n###### {}项目: 数据更新失败".format(project_name))
					else:
						dingNotify("#### 代码安全审计v0.1\n\n###### {}项目: 无内容".format(project_name))
			except Exception as e:
				pass
		else:
			# print("执行扫描, 写入")
			if sonarScan(row) :
				sql =  "insert into sonar_project(id, project_git_id, project_name, project_description, project_path, project_contributors, created_at, updated_at, project_author, department ) value(0, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				tt = DBS.soc_excute(sql, (project_git_id, project_name, project_description, project_path, project_contributors, created_at, updated_at, project_author, department ))
				if tt:
					log(" {}项目: 新增".format(project_name))
					insertBug(row)
				else:
					dingNotify("#### 代码安全审计v0.1\n\n###### {}项目: 新增失败".format(project_name))
			else:
				dingNotify("#### 代码安全审计v0.1\n\n###### {}项目: 无内容".format(project_name))


if __name__ == '__main__':
	# 创建初始数据
	DBS.soc_create()
	while True:
		start = time.time()
		try:
			project_gitlab = GitLAB().getAllProjects()
			project_gerrit = Gerrit()
			project_gitlab.extend(project_gerrit)
			if project_gitlab :
				run(project_gitlab)
				time.sleep(60)
			else:
				time.sleep(60)
		except Exception as e:
			time.sleep(30)

	end = time.time()
	log( " Task %s runs %0.2f seconds." % ("Sonar", (end - start)) )


