# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2018-05-18 10:58:39
# @Author  : Bing (wulitouhaha@vip.qq.com)
# @Link    : http://example.org
# @Desc : 配置信息

import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONAR_SCAN_DIR = os.path.join(BASEDIR, "temp")

# dingding配置
ding_Token = "xxxxxxxxxxxxxxxxxx"
ding_URL = "https://.x.com/"
ding_Data = {
	"grant_type" : "client_credentials", 
	"client_id" : 6,
	"client_secret" : "XVwkwTD4xxxxxxxxx",
	"scope": "*"
}

# git用户配置
git_api = "http://gitlab.x.com/api/v3/"
git_token = {'PRIVATE-TOKEN': 'x-_bJ_b'}
gerrit_url = "http://gerrit.x.com/"
gerrit_ssh_url = "gerrit.x"
git_user = 'x'							
git_pwd = 'xx'

# 配置信息		
sonar_url = 'http://sonar.x.com'
sonar_website_user = 'test'
sonar_website_pwd = 'x'

# 安全中心数据库
soc_mysql_host = "1.1.1.1"
soc_mysql_port = 3306
soc_mysql_user = "x"
soc_mysql_pwd = "x"
soc_mysql_db = "x"

# sonar平台数据库
sonar_host = "1.1.1.1"
sonar_port = 3306
sonar_user = "x"
sonar_pwd = "x"
sonar_db = "x"

