from exts import db

class Article(db.Model):
    __tablename__='article'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    text=db.Column(db.Text,nullable=False)
    article_id=db.Column(db.Integer,db.ForeignKey('new.id'),nullable=False)
    new=db.relation('New',backref=db.backref('articles'))

class New(db.Model):
    __tablename__='new'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    url= db.Column(db.String(400),nullable=False,unique=True)
    headline= db.Column(db.String(400),nullable=False)
    summary = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(400), nullable=False)
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email_address=db.Column(db.String(50),nullable=False)
    username=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    chose_sort=db.Column(db.String(1000))