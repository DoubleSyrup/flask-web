# encoding:utf-8
from functools import wraps
from flask import session,redirect,url_for,render_template,flash

#限制资源登录查看
def login_limit(func):

    @wraps(func)
    def wapper(*args,**kwargs):
        if session.get('user_id'):
            flash("Welcome %s"%session.get('user_id'))
            return func(*args,**kwargs)
        else:
            return render_template('index_nologin.html')
    return wapper