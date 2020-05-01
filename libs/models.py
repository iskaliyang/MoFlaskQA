from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from application import db


class User(db.Model):
    """
    用户模型
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, *args, **kwargs):
        # 拦截信息
        self.email = kwargs.get('email')
        self.username = kwargs.get('username')
        self.password = generate_password_hash(kwargs.get('password'))

    # 检查密码
    def check_pwd(self, pwd):
        return check_password_hash(self.password, pwd)


class Question(db.Model):
    """
    问答模型
    """
    __tablename__ = 'question'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(100), default='python')  # 标签
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 外键
    # 用户模型可以通过questions获取自己所有的发布问答
    author = db.relationship('User', backref=db.backref('questions'))  # 关联关系


class Comment(db.Model):
    """
    评论模型
    """
    __tablename__ = 'comment'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    support = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # Question可以通过comments获取全部问题评论
    question = db.relationship('Question', backref=db.backref('comments', order_by=id.desc()))  # 根据id降序排序返回值
    author = db.relationship('User', backref=db.backref('comments'))  # User可以通过comments获取全部用户的评论
