from flask_login import login_required, current_user
from flask import render_template, flash, request, redirect, url_for, current_app
from sqlalchemy import or_

from app import db
from app.forms.book import DriftForm
from app.libs.email import send_email
from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.spider.drift import DriftViewModel
from . import web

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    form = DriftForm(request.form)
    current_gift = Gift.query.get_or_404(gid)

    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的^_^, 不能向自己索要书籍噢')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    if not current_user.can_send_gift():
        return render_template("not_enough_beans.html", beans=current_user.beans)
    gifter = current_gift.user.summary
    if request.method == "POST" and form.validate():
        drift = Drift()
        drift.save_drift(form, current_gift)
        send_email(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                   wisher=current_user,
                   gift=current_gift)
        return redirect(url_for("web.pending"))
    return render_template("drift.html", gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/pending/')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)
    ).order_by(
        Drift.create_time.desc()
    ).all()
    drifts = DriftViewModel.pending(drifts, current_user.id)
    return render_template("pending.html", drifts=drifts)


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Reject
        db.session.add(drift)
        user = User.query.get(drift.requester_id)
        user.beans += 1
        db.session.add(user)
    return redirect(url_for("web.pending"))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(request_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        db.session.add(drift)
        current_user.beans += 1
    return redirect(url_for("web.pending"))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    """
        确认邮寄，只有书籍赠送者才可以确认邮寄
        注意需要验证超权
    """
    with db.auto_commit():
        # requester_id = current_user.id 这个条件可以防止超权
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += 1
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True
        # 不查询直接更新;这一步可以异步来操作
        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
                             launched=False).update({Wish.launched: True})
    return redirect(url_for('web.pending'))
