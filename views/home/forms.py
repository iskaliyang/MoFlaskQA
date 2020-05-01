# coding: utf8
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from wtforms.fields import TextAreaField
from wtforms.fields import StringField
from wtforms.fields import PasswordField
from wtforms.fields import FileField

from wtforms.validators import DataRequired, ValidationError
from wtforms.validators import EqualTo  # 字段比较
from wtforms.validators import Email  # 邮箱验证
from wtforms.validators import Regexp  # 正则

from libs.models import User


class RegisterForm(FlaskForm):
    username = StringField(
        label='昵称',
        validators=[
            DataRequired('请输入昵称！'),
        ],
        description='昵称',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入昵称！',
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱！'),
            # 验证当前字段是否符合邮箱格式
            Email(message='邮箱格式不正确！')
        ],
        description='邮箱',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入邮箱！'
        }
    )
    pwd1 = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！'),
        ],
        description='密码',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入密码！'
        }
    )
    pwd2 = PasswordField(
        label='确认密码',
        validators=[
            DataRequired('请输入确认密码！'),
            # 验证器
            EqualTo('pwd', message='两次密码不一致！')
        ],
        description='确认',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入确认密码！'
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            'class': 'btn btn-lg btn-success btn-block',
        }
    )

    # 验证昵称的唯一性
    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError(message='昵称已存在！')

    # 验证邮箱的唯一性
    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError(message='邮箱已存在！')

    # 验证电话的唯一性
    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError(message='手机号码已存在！')


class LoginForm(FlaskForm):
    name = StringField(
        label='账号',
        validators=[
            DataRequired('请输入账号！'),
        ],
        description='账号',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入账号！',
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！'),
        ],
        description='密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码！'
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            'class': 'btn btn-lg btn-success btn-block',
        }
    )


class UserDetailForm(FlaskForm):
    name = StringField(
        label='账号',
        validators=[
            DataRequired('请输入账号！'),
        ],
        description='账号',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入账号！',
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱！'),
            # 验证当前字段是否符合邮箱格式
            Email(message='邮箱格式不正确！')
        ],
        description='邮箱',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入邮箱！'
        }
    )
    phone = StringField(
        label='手机',
        validators=[
            DataRequired('请输入手机！'),
            # 正则匹配手机号码
            Regexp('1[3458]\d{9}', message='手机格式不正确！')
        ],
        description='手机',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入手机！'
        }
    )
    face = FileField(
        label='头像',
        validators=[
            DataRequired('请上传头像')
        ],
        description='头像',

    )
    # 简介文本域
    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired('请输入简介！')
        ],
        description='简介',
        render_kw={
            'class': 'form-control',
            'rows': 10,  # 显示10行
        }
    )
    submit = SubmitField(
        '保存修改',
        render_kw={
            'class': 'btn btn-success',
        }
    )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码！')
        ],
        description='旧密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入旧密码！',
            # 'required': 'required'
        }
    )
    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码！')
        ],
        description='新密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入新密码！',
            # 'required': 'required'
        }
    )
    # 提交字段
    submit = SubmitField(
        label='修改密码',
        render_kw={
            'class': 'btn btn-success',  # 表单的样式属性
        }
    )


class CommentForm(FlaskForm):
    content = TextAreaField(
        label='内容',
        validators=[
            DataRequired('请输入内容！')
        ],
        description='内容',
        render_kw={
            'id': 'input_content'
        }
    )
    submit = SubmitField(
        label='提交评论',
        render_kw={
            'class': 'btn btn-success',  # 表单的样式属性
            'id': 'btn-sub'
        }
    )
