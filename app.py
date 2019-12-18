# encoding:utf-8

from flask import Flask,render_template,request,redirect,url_for,session,make_response,jsonify
import config
from models import User,Question
from exts import db
import os
from decorators import login_limit
from datetime import datetime
from werkzeug.utils import secure_filename
import random
import base64

basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
app.secret_key=os.urandom(24)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#获取用户上传图片，存储在本地路径，拼接url，将url存储进数据库
def img_url():
    file_dir = 'D:/PycharmProject/flask-project/flask_zhiliao/static/user_images/'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['content-img']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]
        new_filename = str(random.randint(1,10000000000)) + '.' + ext
        f.save(os.path.join(file_dir, new_filename))
        return '../static/user_images/'+new_filename
    else:
        return "../static/user_images/None"


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

#发布的内容只有登录后才能查看
@app.route('/')
@login_limit
def index():
    context={
        'questions': Question.query.order_by('create_time').all()
    }
    return render_template("index.html",**context)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        sql_phone = User.query.filter(User.phone == username).first()
        sql_username = User.query.filter(User.username == username).first()
        if sql_phone or sql_username:
            sql_password = User.query.filter(User.password == password).first()
            if sql_password:
                session['user_id'] = sql_username.id
                session.permanent = True
                return redirect(url_for("index"))
            else:
                return "密码错误，请从新输入"
        else:
            return '用户不存在，请注册'

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for("login"))

@app.route('/regist',methods=['GET','POST'])
def regist():
    if request.method == "GET":
        return render_template("regist.html")
    else:
        phone = request.form.get('phone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #验证手机号是否已存在
        user = User.query.filter(User.phone == phone).first()
        if user:
            return '手机号已存在'
        else:
            if password1 != password2:
                return '两次输入密码不一致，请重新输入'
            else:
                user = User(phone=phone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return "注册成功"

@app.route('/question',methods=['GET','POST'])
@login_limit
def question():
    # user_id = session.get('user_id')
    # if user_id:
    #     return render_template('talking.html')
    # else:
    #     return render_template('login.html')
    if request.method == 'GET':
        return render_template('talking.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        imgurl = img_url()
        question = Question(title=title,create_time= datetime.now(),content=content,imgurl=imgurl)
        user_id = session.get('user_id')
        user = User.query.filter(User.id==user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.context_processor
def my_context():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
