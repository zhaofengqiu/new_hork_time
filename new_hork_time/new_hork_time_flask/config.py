SECRET_KEY='a secret key'
DEBUG = True
HOSTNAME='xxx'
PORT    ='xxx'
DATABASE='xxx'
USERNAME='xxx'
PASSWORD='xxx'
SQLALCHEMY_TRACK_MODIFICATIONS=False
DB_URI  ='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,
        HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI=DB_URI


