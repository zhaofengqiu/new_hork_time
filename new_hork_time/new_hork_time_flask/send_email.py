from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config,time
from models import Article,New,User
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("temp.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
mode="""

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>News</title>
    <style type="text/css"> 
    body{background: #ffffff;overflow:scroll;} 
    .main{background: #fff;width: 730px;margin: 0 auto;overflow: hidden;padding: 10px;}
    hr {margin-top:7px;*margin: 0;border: 0;color: #FFF;background-color: black;height: 3px}
    .css-1i0edl6{font-weight:600;font-size:18px;font-family:SimSun}
    img{border:20px solid #FFF}
    </style> 
    <meta name="viewport" content="width=device-width,height=device-height,initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
</head>
<body background='#ffffff' overflow='scroll'>
    <div class="main" background=#fff width=730px margin=0 auto overflow=hidden padding=10px>
    <h1 align="center">%s</h1>
    %s
    </div>
</body>

</html>
"""

from email.mime.text import MIMEText
from email.header import Header

import smtplib
global session
def send_email():
    global session
    logger.info('send email start----------')
    from_addr='xxxx'
    password='xxxx'#授权码
    smtp_server='smtp.qq.com'
    smtpport='465'
    users=get_user()#这里获取到的user是一个model,是数据库中的类
    smtp = smtplib.SMTP_SSL(smtp_server, smtpport)
    smtp.login(from_addr, password)
    for user in users:
        logger.info('%s send_email start------' % (user.email_address))
        sorts = get_sorts(user.email_address)
        to_addr = user.email_address
        if sorts:
            for sort in sorts.keys():
                print(sort)
                new = session.query(New).order_by(New.datetime.desc()).filter(New.section == sort).first()
                logger.info(new.headline)
                print(mode%(new.headline ,new.articles[0].text))
                msg = MIMEText(mode%(new.headline ,new.articles[0].text), 'html', 'utf-8')
                msg['Subject'] = new.headline
                #smtp.sendmail(from_addr, to_addr,  msg.as_string())
                time.sleep(3)
        logger.info('%s send_email end------'%(user.email_address))
        time.sleep(2)
    smtp.quit()
    logger.info('smtp loginout')
def get_sorts(email_address):
    user=session.query(User).filter_by(email_address=email_address).first()
    if user.chose_sort:
        sorts = eval(user.chose_sort)
        return sorts

    else:
        return None

def get_user():


    return session.query(User).all()

def clear_all_news():

        session.query(Article).delete()
        session.query(New).delete()
        session.commit()

def init():
    engine = create_engine(config.DB_URI)
    DBSession = sessionmaker(bind=engine)
    session=DBSession()
    return session
session = init()
if __name__== "__main__":
    send_email()

