from app.models.gift import Gift
from . import web
from flask import render_template


__author__ = '七月'


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    recent_gifts = [gift.book for gift in recent_gifts]
    return render_template("index.html", recent=recent_gifts)


@web.route('/personal')
def personal_center():
    pass
