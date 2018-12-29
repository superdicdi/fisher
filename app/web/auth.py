from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from app import db
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.libs.email import send_email
from app.models.user import User
from app.web import web

__author__ = '涂迪'


@web.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for("web.login"))
    return render_template("auth/register.html", form=form)


@web.route('/login/', methods=['GET', 'POST'])
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


@web.route('/reset/password/', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == "POST" and form.validate():
        user = db.session.query(User).filter(User.email == form.email.data).first_or_404()
        send_email(form.email.data, "重置你的密码", "email/reset_password.html", user=user, token=user.generate_token())
        flash("邮件已发送，请在邮箱中查看~")
    return render_template("auth/forget_password_request.html")


@web.route('/reset/password/<token>/', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == "POST" and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash("密码设置成功，请重新登录")
            return redirect(url_for("web.login"))
        flash("链接已失效，请重新申请")
        return redirect(url_for("web.forget_password_request"))
    return render_template("auth/forget_password.html", form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for("web.login"))
