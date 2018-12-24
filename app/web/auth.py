from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user
from app import db
from app.forms.auth import RegisterForm, LoginForm
from app.models.user import User
from app.web import web

__author__ = '涂迪'


@web.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("web.login"))
    return render_template("auth/register.html", form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        data = form.data
        user = User.query.filter_by(nickname=data["nickname"]).first()
        if user and user.check_password(data["password"]):
            login_user(user, remember=True)
            next_url = request.args.get("next")
            if not next_url or not next_url.startswith("/"):
                next_url = url_for("web.search")
            return redirect(next_url)
        flash("账号或密码错误")
    return render_template("auth/login.html", form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    pass
