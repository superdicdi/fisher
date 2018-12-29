from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app import db
from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.models.gift import Gift
from app.spider.mygifts import MyGifts
from . import web

__author__ = '涂迪'


@web.route('/my/gifts/')
@login_required
def my_gifts():
    gifts = Gift.query.filter_by(uid=current_user.id, launched=False).all()
    gift_isbns = [gift.isbn for gift in gifts]
    wish_count = Gift.get_wish_counts(gift_isbns)
    my_gift = MyGifts()
    gifts = my_gift.search_by_isbns(gifts, wish_count)
    return render_template("my_gifts.html", gifts=gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config["BEANS_UPLOAD_BOOK"]
            db.session.add(gift)
    else:
        flash("这本书已添加至你的赠送清单或已存在于你的心愿清单")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/gifts/<gid>/redraw/')
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, _pending=1).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂完成该交易')
    else:
        with db.auto_commit():
            current_user.beans -= 0.5
            gift.delete()
            db.session.add(gift)
    return redirect(url_for('web.my_gifts'))
