# Code Security Detection
[![License](https://img.shields.io/:license-gpl3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/Canbing007/wukong-agent)
[![python](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/)

## Structure Design
![workflow](http:///CodeScan/raw/master/screen/webcode7.png)

## Requirement
环境要求[linux系统]:    
python3      
mysql    
sonar-scanner-cli     

## DirIntroduce
```
├── codescan.log 			# 日志记录文件
├── CodeScan.py 			# 程序入口
├── core 					# 配置文件目录
│   ├── __init__.py
│   └── settings.py
├── lib 					# 公共文件目录
│   ├── common.py
│   ├── database.py
│   ├── __init__.py
│   ├── logger.py
├── README.md 			
├── requirements.txt
├── rule 					# sonarqube自定义规则模板
│   ├── sonar-custom-rule
├── temp 					# 项目扫描临时存放目录
├── test
│   └── 11.py
├── thirdparty 				# 第三方工具目录
│   └── sonar        		# sonarqube扫描器
└── utils 					# 其它工具调用目录
    ├── excute.py
    ├── gitlab.py
    ├── __init__.py
```


## Configure
#### 配置基本信息
```
# 克隆项目
git clone https://github.com/Canbing007/CodeScan.git

# 安装git
yum install git

# 安装python依赖包
pip install requirements.txt

### 配置项目信息

# dingding配置
ding_Token = "xx"
ding_URL = "https://xx.com/"
ding_Data = {
	"grant_type" : "client_credentials", 
	"client_id" : 3,
	"client_secret" : "xx",
	"scope": "*"
}

# git用户配置和gerrit配置
git_api = "http://git.xxx.com/api/v3/"
git_token = {'PRIVATE-TOKEN': 'xxx-_bJ_b'}
git_user = 'xx'							
git_pwd = 'xx'

# 配置信息		
sonar_url = 'http://sonar.xx.com'
sonar_website_user = 'xx'
sonar_website_pwd = 'xx'

# 数据库可配置
soc_mysql_host = "127.0.0.1"
soc_mysql_port = 3306
soc_mysql_user = "xx"
soc_mysql_pwd = "xx"
soc_mysql_db = "xx"

sonar_host = "192.168.1.1"
sonar_port = 3306
sonar_user = "xx"
sonar_pwd = "xx"
sonar_db = "xx"

```


#### Usage
```
# 赋予项目的sonar脚本有执行权限
chmod -R +x CodeScan 

# 配置内存信息
linux防止内存报错：
export SONAR_SCANNER_OPTS="-Xmx512m"   
windows防止内存报错：
set SONAR_SCANNER_OPTS=-Xmx512m

# 配置gitlab和gerrit  
1.在gitlab和gerrit上的新建一个扫描账户，把扫描账户添加成为每个项目的一员，具有拉取项目权限
2.在git的机器上配置好ssh-key,以便拉取项目

# 执行如下命令
python3 CodeScan.py  
```

#### Todo
1.并发扫描测试   

