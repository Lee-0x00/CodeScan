# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Date    : 2018-05-18 10:58:39
# @Author  : Bing (wulitouhaha@vip.qq.com)
# @Link    : http://example.org
# @Desc : $Id$

import sys
sys.path.append('..')

import logging, os
from core.settings import BASEDIR
# from colorama import  init, Fore, Back, Style

def log(message):
	logger = logging.getLogger(__name__)
	logger.setLevel(level = logging.INFO)
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	# 保存日志文件
	handler = logging.FileHandler("{}".format(os.path.join(BASEDIR, "codescan.log")))
	handler.setFormatter(formatter)
	handler.setLevel(logging.INFO)
	# 终端日志显示
	console = logging.StreamHandler()
	console.setFormatter(formatter)
	console.setLevel(logging.INFO)

	logger.addHandler(handler)
	logger.addHandler(console)
	logger.info(message)
	logger.removeHandler(console)
	logger.removeHandler(handler)

# init(autoreset=True)  

# class Colored(object):  
# 	#  前景色:红色  背景色:默认
# 	@staticmethod
# 	def red(s):  
# 		return Fore.RED + s + Fore.RESET  

# 	#  前景色:绿色  背景色:默认  
# 	@staticmethod
# 	def green(s):  
# 		return Fore.GREEN + s + Fore.RESET  

# 	#  前景色:黄色  背景色:默认  
# 	@staticmethod
# 	def yellow(s):  
# 		return Fore.YELLOW + s + Fore.RESET  

# 	#  前景色:蓝色  背景色:默认  
# 	@staticmethod
# 	def blue(s):  
# 		return Fore.BLUE + s + Fore.RESET  

# 	#  前景色:洋红色  背景色:默认  
# 	@staticmethod
# 	def magenta(s):  
# 		return Fore.MAGENTA + s + Fore.RESET  

# 	#  前景色:青色  背景色:默认  
# 	@staticmethod
# 	def cyan(s):  
# 		return Fore.CYAN + s + Fore.RESET  

# 	#  前景色:白色  背景色:默认  
# 	@staticmethod
# 	def white(s):  
# 		return Fore.WHITE + s + Fore.RESET  

# 	#  前景色:黑色  背景色:默认  
# 	@staticmethod
# 	def black(s):  
# 		return Fore.BLACK  

# 	#  前景色:白色  背景色:绿色  
# 	@staticmethod
# 	def white_green(s):  
# 		return Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET 
