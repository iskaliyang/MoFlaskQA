import json
import traceback
import re
from functools import wraps

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, g
from sqlalchemy import or_

from application import db, app
from libs.models import User, Question

home = Blueprint('home', __name__)


# db.init_app(app)


@home.route('/', methods=['GET', 'POST'])
def index():
    """
    网站首页
    :return:
    """
    context = {
        'questions': Question.query.order_by(db.desc('create_time')).all()  # 按照时间降序排序 最新的信息在排在前面
    }
    return render_template('home/index.html', **context)


@home.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录
    :return:
    """
    if request.method == 'GET':
        return render_template('home/login.html')
    elif request.method == 'POST':
        # 1. 获取数据
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        remember = request.form.get('remember')

        # 2. 检查数据
        user = User.query.filter(User.email == email).first()
        if user and user.check_pwd(pwd):
            # 3. 业务处理
            # 保存cookie
            session['user_id'] = user.id
            # 三十天内不要登录
            if remember == 'on':
                session.permanent = True
            return redirect(url_for('home.index'))
        else:
            return render_template('home/login.html', errmsg='账号或密码错误')


@home.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册
    :return:
    """
    if request.method == 'GET':
        return render_template('home/register.html')
    elif request.method == 'POST':
        # 1. 获取提交数据
        username = request.form.get('username')
        email = request.form.get('email')
        pwd1 = request.form.get('pwd1')
        pwd2 = request.form.get('pwd2')
        # 2.检查数据
        if not all([username, email, pwd1, pwd2]):
            return render_template('home/register.html', errmsg='请填写完整信息')
        # ^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+
        email_re = '^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
        if not re.match(email_re, email):
            return render_template('home/register.html', errmsg='邮箱格式不正确')

        if pwd1 != pwd2:
            return render_template('home/register.html', errmsg='两次密码不一致')

        db_email = User.query.filter_by(email=email).first()
        if db_email:
            return render_template('home/register.html', errmsg='邮箱已存在')

        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('home/register.html', errmsg='昵称已存在')

        # 3.业务处理
        try:
            # 密码自己加密 这里不加密
            user = User(username=username, email=email, password=pwd1)
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            traceback.print_exc()

        return redirect(url_for('home.login'))


@home.route('/logout/')
def logout():
    """
    退出登录 30天内自动登录失效
    :return:
    """
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('home.index'))


@home.route('/search/')
def search():
    """
    搜索
    :return:
    """
    q = request.args.get('q')
    if q is not None:
        # 标题或内容包含有都返回
        questions = Question.query.filter(or_(Question.title.contains(q), Question.content.contains(q))).order_by(
            db.desc('create_time')).all()
        return render_template('home/index.html', questions=questions)
    else:
        pass


@home.context_processor
def check_login():
    """
    上下文处理器
    :return:
    """
    # user_id = session['user_id']  #  这种方式获取如果user_id不存在则抛出异常
    user_id = session.get('user_id')  # 这种方式则没有user_id则返回none
    # 如果用户登录了
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if user:
            # 把数据存储到模板上下文 模板可以通过{{ user }}方式使用数据
            return {'user': user}
    else:
        return {}


# # 每次请求之前都会执行这个函数
# @home.before_request
# def deal_info():
#     user_id = session.get('user_id')
#     if user_id:
#         user = User.query.filter_by(id=user_id).first()
#         # g:应用程序上下文
#         if user:
#             g.user = user
