import datetime

import flask
from flask_login import login_user, login_required, current_user, user_logged_out, logout_user
from forms import LoginForm, SignUpForm, WriteForm
from flask import redirect, url_for, render_template, flash, request, g, current_app

from init_ import db, app, login_manager
from models import User, Post


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.before_request
def before_request():#在请求提交之前会执行本函数
    g.user = current_user
@app.route('/user/<id><int:page>',methods = ['GET'])
@app.route('/user/<id>',methods = ['GET'])
@login_required
def user(id,page = 1):
    user = User.query.filter(id == id).first()
    post = Post.query.filter(Post.user_id == id).order_by(db.desc(Post.time)).paginate(page,per_page=3,error_out=False)
    return render_template('user.html',user = user,post = post)
@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()#创建自定义表单实例
    if form.validate_on_submit():
        user = User.login_check(form.username.data,form.password.data)
        if user:
            login_user(user)
            user.last = datetime.datetime.now()
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash('Database Error!')
                return redirect('/login')
            return redirect(url_for('index'))
        else:
            return redirect('/login')
    return render_template('login.html', form = form)

@app.route('/index/<int:page>',methods=['GET'])
@app.route('/index',methods=['GET'])
@login_required
def index(page = 1):
    post = Post.query.filter(db.and_(Post.user_id == current_user.id)).order_by(db.desc(Post.time)).paginate(page,per_page=3,error_out=False)
    return render_template('index.html',title='Home',post = post)

@app.route('/detail/<post>')
@login_required
def detail(post):
    p_content = Post.query.filter(Post.id == post).first()
    return render_template('detail.html', p_content = p_content)

@app.route('/',methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/write',methods=['GET',"POST"])
@login_required
def write():
    form = WriteForm()
    if form.validate_on_submit():
        post = Post()
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.time = datetime.datetime.now()
        post.user_id = current_user.id
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('write.html',form = form)

@app.route('/edit/<post_id>',methods = ['GET','POST'])
@login_required
def edit(post_id):
    form = WriteForm()
    post = Post.query.filter(Post.id == post_id).first()
    form.title.data = post.title
    form.content.data = post.content
    if form.validate_on_submit():
        post.title = request.form.get("title")
        post.content = request.form.get("content")
        post.time = datetime.datetime.now()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('user',id = current_user.id))
    return render_template('edit.html',form = form,post = post)

@app.route("/<name>/<profession>/<sex>/<city>/<birthday>/<introduce>",methods=['GET','POST'])
@login_required
def change(name,profession,sex,city,birthday,introduce):
    current_user.name = name
    current_user.profession = profession
    current_user.sex = sex
    current_user.city = city
    current_user.birthday = birthday
    current_user.introduce = introduce
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for("/user",id = current_user.id))

@app.route('/sign_up',methods = ['GET','POST'])
def sign_up():
    form = SignUpForm()
    user = User()
    if form.validate_on_submit():
        print("打印了")
        username = request.form.get('username')
        password = request.form.get('password')
        register_check = User.query.filter(db.and_(User.name == username, User.password == password)).first()
        if register_check:
            return redirect('/sign_up')
        else:
            user.name = username
            user.password = password
            db.session.add(user)
            db.session.commit()
            next = flask.request.args.get('next')
            return redirect(next or url_for('index'))
    return render_template('sign_up.html',form=form)