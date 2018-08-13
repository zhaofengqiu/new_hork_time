from flask import Flask,render_template,url_for,redirect,request,session
#from funtions import *
from flask_debugtoolbar import DebugToolbarExtension
import os,re
import config
app = Flask(__name__)
app.config.from_object(config)
app.config['SECRET_KEY']=os.urandom(12)
#print(config.DB_URI)
from exts import db
from models import Article, User ,New
db.init_app(app)
sorts=['Top_new','World','U.S.','Politics','N.Y.','Business','Opinion',
      'Tech','Science','Health','Sports','Arts','Books',
      'Style','Food','Travel','Magazine']
mail_names = open(r'C:\Users\asus\Desktop\myproject_old\new_hork_timetemp\mail_names.txt').readlines()
@app.route('/')
def hello_world():
    return redirect('/index/')

@app.route('/index/')
def index():

    datas = New.query.order_by(New.datetime.desc()).filter(New.section == 'Top_new').limit(20)

    data = {'kind': 'Top_new',
            'dat': datas}
    return render_template('section.html', new_data=data)

@app.route('/section/<sort>')
def section(sort):
    datas = New.query.order_by(New.datetime.desc()).filter(New.section == sort).limit(20)
    data={'kind':sort,
          'dat':datas}
    return render_template('section.html',new_data=data)

@app.route('/detail/<article_id>')#<>里面放的是变量名
def detail(article_id):
    article=Article.query.filter(Article.article_id == article_id).first()
    return render_template('detail.html',articledata=article)
@app.route('/news_data/<article_id>')
def new_york_data(article_id):

    article = Article.query.filter(Article.article_id == article_id).first()
    return render_template('news_data.html', articledata=article)
@app.route('/register/',methods={'GET','POST'})
def register():

    if request.method=='GET':
        return render_template('register.html')
    elif request.method=='POST':
        email_adress=request.form.get('email_adress')
        username=request.form.get('username')
        pwd1=request.form.get('password1')
        pwd2=request.form.get('password2')
        user=User.query.filter(User.email_address==email_adress).first()
        if user :
            return u'该用户已经注册'
        elif pwd1!=pwd2:
            return u'第一次和第二次密码不一致'
        else:
            ans=verify_mail_name(email_adress)
            if ans==1:

                return u'邮箱格式不符'
            elif ans==2:

                return u'该邮箱类型目前暂不提供订阅服务'

            elif ans==3:
                user = User(email_address=email_adress, username=username, password=pwd1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/login/',methods={'GET','POST'})
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        username=request.form.get('username')
        pwd=request.form.get('password')
        user1=User.query.filter(User.username==username,User.password==pwd).first()
        user2=User.query.filter(User.email_address == username, User.password == pwd).first()

        if user1 or user2:
            if user1:
                session['username']= user1.username
            if user2:
                session['username'] = user2.username
            return  redirect(url_for('user'))
        else:
            user1 = User.query.filter(User.username == username).first()
            user2 = User.query.filter(User.email_address == username).first()

            if user1 or user2:
                return u'密码错误'

            else:

                return u'用户未注册'
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/user/',methods=['GET','POST'])
def user():
    if request.method=='GET':
        if session.get('username'):
            user = User.query.filter(User.username == session.get('username')).first()
            if user.chose_sort:
                data=eval(user.chose_sort)
            else:
                data={}
            data['username']=session.get('username')
            return render_template('user.html',data=data,sort=sorts)
        else:

            return redirect(url_for('index'))
    else:
        user=User.query.filter(User.username==session.get('username')).first()
        requests_sort = request.form.to_dict()
        if user.chose_sort:
            user_sort = eval(user.chose_sort)
        else:
            user_sort = {}
        if requests_sort['upgrade']=='cancle':
            user=User.query.filter(User.username==session.get('username')).first()
            db.session.delete(user)
            db.session.commit()
            session.clear()
            return redirect('/index/')
        else:

            if requests_sort['upgrade']=='up':

                for key,value in list(requests_sort.items()):
                    if value=='on':
                        user_sort[key]=value

            elif requests_sort['upgrade']=='down':
                requests_sort=request.form.to_dict()
                for key,value in list(requests_sort.items()):
                    if value=='on':
                        user_sort.pop(key)
            user.chose_sort=str(user_sort)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user'))
@app.context_processor
def my_context_processor():
    username=session.get('username')
    if username:
        user=User.query.filter(User.username==username).first()
        if user:
            return {'user':user.username}
    return {}
def verify_mail_name(mail_addr):
    if re.search('@',mail_addr)==None:
        return 1
    for mail_name in mail_names:
        if re.search(mail_name.replace('\n',''), mail_addr, re.S):
            return 3

    return 2
if __name__ == '__main__':
    toolbar=DebugToolbarExtension(app)
    app.run()

