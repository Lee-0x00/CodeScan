# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2018-05-18 10:58:39
# @Author  : Bing (wulitouhaha@vip.qq.com)
# @Link    : http://example.org
# @Desc : database operation

import sys
sys.path.append('..')

import pymysql
from core.settings import *


class Database(object):
	"""docstring for sql operation """
	def __init__(self):
		# 安全服务
		self.soc_mysql_host = soc_mysql_host
		self.soc_mysql_port = soc_mysql_port
		self.soc_mysql_user = soc_mysql_user
		self.soc_mysql_pwd = soc_mysql_pwd
		self.soc_mysql_db = soc_mysql_db
		self.soc_mysql_charset = "utf8"
		self.soc_cursor, self.soc_db = self.soc_connect()

		# 扫描服务
		self.sonar_host = sonar_host
		self.sonar_port = sonar_port
		self.sonar_user = sonar_user
		self.sonar_pwd = sonar_pwd
		self.sonar_db = sonar_db
		self.sonar_charset = "utf8"
		self.sonar_cursor, self.sonar_db = self.sonar_connect()


	def soc_connect(self):
		soc_db = pymysql.connect(host=self.soc_mysql_host,	port=self.soc_mysql_port, user=self.soc_mysql_user, password=self.soc_mysql_pwd, db=self.soc_mysql_db, charset=self.soc_mysql_charset)
		cursor = soc_db.cursor()
		return cursor, soc_db


	def sonar_connect(self):
		sonar_db = pymysql.connect(host=self.sonar_host,	port=self.sonar_port, user=self.sonar_user, password=self.sonar_pwd, db=self.sonar_db, charset=self.sonar_charset)
		sonar_cursor = sonar_db.cursor()
		return sonar_cursor, sonar_db


	def soc_create(self):
		try:
			# 项目列表
			sql = """CREATE TABLE `sonar_project` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`project_git_id` varchar(50) DEFAULT NULL,
					`project_name` varchar(800) DEFAULT NULL,
					`project_description` varchar(2000) DEFAULT NULL,
					`project_path` varchar(800) DEFAULT NULL,
					`project_contributors` varchar(800) DEFAULT NULL,
					`created_at` varchar(800) DEFAULT NULL,
					`updated_at` varchar(800) DEFAULT NULL,
					`project_author` varchar(50) DEFAULT NULL,
					`department` varchar(20) DEFAULT NULL,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;
			"""
			self.soc_cursor.execute(sql)
			self.soc_db.commit()

			# 漏洞列表
			sql = """CREATE TABLE `sonar_codebug` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`project_name` varchar(800) DEFAULT NULL,
					`project_sonar_id` varchar(50) DEFAULT NULL,
					`bug_id` varchar(50) DEFAULT NULL,
					`bug_name` varchar(200) DEFAULT NULL,
					`bug_type` varchar(50) DEFAULT NULL,
					`bug_severity` varchar(20) DEFAULT NULL,
					`bug_fix_status` varchar(800) DEFAULT NULL,
					`bug_ctime` varchar(800) DEFAULT NULL,
					`bug_ftime` varchar(800) DEFAULT NULL,
					`linkid` varchar(500) DEFAULT NULL,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;
			"""
			self.soc_cursor.execute(sql)
			self.soc_db.commit()
			return True
		except Exception as e:
			# print(e)
			return False


	def soc_selectone(self, sql, value):
		try:
			self.soc_cursor.execute(sql, value)
			data = self.soc_cursor.fetchone()
			return data
		except Exception as e:
			# print(e)
			return False


	def soc_select(self, sql, value):
		try:
			self.soc_cursor.execute(sql, value)
			data = self.soc_cursor.fetchall()
			return data
		except Exception as e:
			# print(e)
			return False


	def soc_excute(self, sql, value):
		try:
			self.soc_cursor.execute(sql, value)
			self.soc_db.commit()
			return True
		except Exception as e:
			# print(e)
			return False


	def soc_close(self):
		try:
			self.soc_cursor.close()
			self.soc_db.close()
			return True
		except Exception as e:
			# print(e)
			return False


	# sonar数据操作
	def sonar_selectone(self, sql, value):
		try:
			self.sonar_cursor.execute(sql, value)
			data = self.sonar_cursor.fetchone()
			return data
		except Exception as e:
			# print(e)
			return False


	def sonar_select(self, sql, value):
		try:
			self.sonar_cursor.execute(sql, value)
			data = self.sonar_cursor.fetchall()
			return data
		except Exception as e:
			# print(e)
			return False


	def sonar_excute(self, sql, value):
		try:
			self.sonar_cursor.execute(sql, value)
			self.sonar_db.commit()
			return True
		except Exception as e:
			# print(e)
			return False


	def sonar_close(self):
		try:
			self.sonar_cursor.close()
			self.sonar_db.close()
			return True
		except Exception as e:
			# print(e)
			return False

