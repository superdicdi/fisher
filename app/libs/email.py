from threading import Thread

from flask import render_template
from flask_mail import Message

from app import mail, app

__author__ = "TuDi"
__date__ = "2018/12/27 下午2:13"


def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    message = Message("[鱼书]" + " " + subject, body="正文", recipients=[to])
    message.html = render_template(template, **kwargs)
    thread = Thread(target=send_async_email, args=[message])
    thread.start()
