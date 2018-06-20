# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2018-05-18 10:58:39
# @Author  : Bing (wulitouhaha@vip.qq.com)
# @Link    : http://example.org
# @Desc : execute command 

import sys
sys.path.append('..')

import subprocess, os, stat
from core.settings import *
from lib.common import delDir

def pull(project_git_id, git_project_url, git_matser_path):
	if project_git_id == "gerrit-000-00":
		# 执行命令
		cmd = ['git', 'clone', git_project_url]
		p = subprocess.Popen(cmd, cwd = git_matser_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p.wait()
	else:
		# 克隆项目
		str_list = list(git_project_url)
		str_list.insert(7,'{}:{}@'.format(git_user, git_pwd)) 		
		git_url = "".join(str_list)
		# 执行命令
		cmd = ['git', 'clone', git_url]
		p = subprocess.Popen(cmd, cwd = git_matser_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p.wait()
	return True


def scan(project_git_id, git_project_name, git_project_dir):
	configureFile = os.path.join(git_project_dir,'sonar-project.properties')
	if os.path.exists(git_project_dir):
		if os.path.exists(configureFile):
			os.remove(configureFile)
	else: 
		return False
		
	# 建立配置文件sonar-project.properties
	f = open(configureFile, 'a+')
	f.write('sonar.host.url={}\n'.format(sonar_url))   		
	f.write('sonar.login={}\n'.format(sonar_website_user))						
	f.write('sonar.password={}\n'.format(sonar_website_pwd))
	if project_git_id == "gerrit-000-00":		
		f.write('sonar.projectKey=gerrit_{}\n'.format(git_project_name))	
		f.write('sonar.projectName=gerrit_{}\n'.format(git_project_name))	
	else:				
		f.write('sonar.projectKey={}\n'.format(git_project_name))	
		f.write('sonar.projectName={}\n'.format(git_project_name))				
	f.write('sonar.projectVersion=1.0\n') 					  			
	f.write('sonar.sources=.\n')
	f.write('sonar.sourceEncoding=UTF-8\n')
	f.write('sonar.java.binaries=.\n')
	f.write('sonar.java.libraries=.\n')
	f.close()

	# 执行扫描
	scanner_cmd = os.path.join(BASEDIR, 'thirdparty/sonar/bin/sonar-scanner')
	cmd = [scanner_cmd,'-X']
	p = subprocess.Popen(cmd,cwd=git_project_dir)
	p.wait()

	return True



