# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import re
from project import app
from exts import db
from models import New,Article
from urllib3 import disable_warnings
import logging
import base64
disable_warnings()
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("temp.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
disable_warnings()
db.init_app(app)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def insertuser(url,headline,summary,datetime,section):#将数据插入数据库中
    global articleurl
    articleurl=url
    with app.app_context():
        try:

            new_old = New(url=url, datetime=datetime, headline=headline, summary=summary,  section=section)
            db.session.add(new_old)
            db.session.commit()
            new = New.query.filter(New.url == url).first()
           
            return new
        except Exception as ce:
          

            logger.error(ce)

def insertarticle(new_id,text):
    with app.app_context():
        try:
            if text=='':

                new = New.query.filter(New.id == new_id).first()
                db.session.delete(new)
            else:

                article = Article(article_id=new_id,text=text)
                db.session.add(article)
            db.session.commit()
            ans = "news_url=%s insert succeed" % (article.new.headline)
          
            logger.info(ans)
            time.sleep(3)
        except Exception as ce:
      
            logger.error(ce)

header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
def getdetail(url, new_id):  # 获取到一篇新闻的文本

    text = '<!---->'

    try:
        r = requests.get(url, verify=False)
        htmldata = BeautifulSoup(r.text, 'html.parser')
        new_texts = htmldata.find_all('p', attrs={'class': 'css-1i0edl6'})
        picture_urls = htmldata.find_all('img')
        split_numble = len(new_texts) // len(picture_urls)
        for i in range(len(new_texts))[1:]:

            if i % split_numble == 0:

                text = text + "<!---->" + str(new_texts[i])

            else:

                text = text + str(new_texts[i])

        new_text = text
        for picture_tag in picture_urls:
            tag = picture_tag.parent
            picture_url = tag.img.attrs['src']
            picture_decrease = tag.next_sibling
            r = requests.get(picture_url, verify=False)
            picture_code = base64.b64encode(r.content)
            picture_code = str(picture_code).replace("b'", '').replace("'", '')
            if picture_decrease == None:
                picture_code = '<img src="data:image/jpeg;base64, %s"/>' % (picture_code)
            else:
                picture_code = '<img src="data:image/jpeg;base64, %s"/>%s<br ><br />' % (picture_code, picture_decrease)

            new_text = re.sub('<!---->', picture_code, new_text, 1, re.S)

        insertarticle(new_id, new_text)

    except Exception as ce:

        logger.error(ce)
def getnews(url,section):#获取到一个大类的信息
    global i, temple
    data=requests.get(url,verify=False).text
    page_data = BeautifulSoup(data, 'html.parser')
    datas = page_data.find_all('div', attrs={'class': 'story-body'})
    for data in datas[:30]:
        headline = ''
        article_url = data.find_all(attrs={'href': True})[0].get('href')
        headlines = data.find_all(attrs={'class': 'headline'})[0].strings
        for text in headlines:
            headline = headline + text
        summary = data.find_all(attrs={'class': 'summary'})[0].string
        datetime = re.findall('com/(\d{1,5}/\d{1,3}/\d{1,3})', article_url)

        if len(url) and len(headline) and len(summary) and len(datetime) and len(section):
       
            new=insertuser(article_url,headline,summary,datetime[0],section)

            if new!=None:

                getdetail(article_url, new.id)

def getindex(url):#获取到首页的信息
    htmldata = requests.get('https://www.nytimes.com', verify=False).text
    data = BeautifulSoup(htmldata, 'html.parser')
    newsdatas = data.find_all('article')
  
    for data in newsdatas[:30]:
        head = ''
        summary = ''
        url = ''
        try:
            url = data.find('a').attrs['href']
            headline = data.find(attrs={'class', 'story-heading'}).get_text()
            summary = data.find('p', attrs={'class', 'summary'}).get_text()
            datetime = re.findall('com/(\d{1,5}/\d{1,3}/\d{1,3})', url)
            section = 'Top_new'
        except Exception as ce:
        	logger.error(ce)
        if len(url) and len(headline) and len(summary) and len(datetime) and len(section):
            new=insertuser(url,headline,summary,datetime[0],section)
          
            if new != None:

                getdetail(url,new.id)

    list = re.findall('(<li class="shortcuts-.*?</li>)', htmldata, re.S)
    j=0
    for lis in list:
        li = BeautifulSoup(lis, 'html.parser')
        url = li.a.get('href')
        section = li.a.string
        getnews(url, section)
if __name__ == '__main__':
    logger.info('running start')
    url="https://www.nytimes.com/"
    getindex(url)
    logger.info('running end')