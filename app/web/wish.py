from flask import flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from app import db
from app.libs.email import send_email
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.mywishs import MyWishes
from . import web

__author__ = '七月'


@web.route('/my/wish')
@login_required
def my_wish():
    wishes = Wish.query.filter_by(uid=current_user.id).all()
    wish_isbns = [wish.isbn for wish in wishes]
    gift_count = Wish.get_gift_counts(wish_isbns)
    my_wishes = MyWishes()
    wishes = my_wishes.search_by_isbns(wish_isbns, gift_count)
    return render_template("my_wish.html", wishes=wishes)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash("这本书已添加至你的赠送清单或已存在于你的心愿清单")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
# @limiter.limit(key_func=limit_key_prefix)
def satisfy_wish(wid):
    """
        向想要这本书的人发送一封邮件
        注意，这个接口需要做一定的频率限制
        这接口比较适合写成一个ajax接口
    """
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，请点击“加入到赠送清单”添加此书。添加前，请确保自己可以赠送此书')
    else:
        send_email(wish.user.email, '有人想送你一本书', 'email/satisify_wish.html', wish=wish,
                   gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn).first()
    if not wish:
        flash('该心愿不存在，删除失败')
    else:
        with db.auto_commit():
            wish.status = 0
            db.session.add(wish)
    return redirect(url_for('web.my_wish'))
