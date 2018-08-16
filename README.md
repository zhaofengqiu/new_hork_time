# new_hork_time
## 效果图:  
### 首页  
![](https://github.com/zhaofengqiu/new_hork_time/blob/master/new_hork_time/images/index.png)
### 文章  
![](https://github.com/zhaofengqiu/new_hork_time/blob/master/new_hork_time/images/article.png)
### 爬虫日志  
![](https://github.com/zhaofengqiu/new_hork_time/blob/master/new_hork_time/images/spider_log.png)
## 这个项目分为两部分
1. 第一部分是爬虫部分**new_hork_time_spider**来提供数据;
2. 第二部分是网站部分**new_hork_time_flask**用来搭建一个新闻网站  
### 部署
部署分为两部分部署，第一部分是爬虫的部署，第二部分是网站的部署。  其中你需要两台服务器，一台海外服务器放置爬虫，一台国内服务器部署网站
1. 网站的部署  
 1. 数据库ORM映射
 '''
 python manage.py db init
 python manage.py db migrate
 python manage.py db upgrade
 '''
