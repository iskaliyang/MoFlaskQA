from functools import wraps
from flask import session, redirect, url_for, request


def logon_required(func):
    """
    登录限制装饰器
    :param func: 被装饰的函数
    :return: wrapper函数 而不是wrapper的执行结果
    """
    @wraps(func)  # 防止函数名被修改
    def wrapper(*args, **kwargs):
        # 如果已经登录 可以下一步操作
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:

            return redirect(url_for('home.login'))
    return wrapper
