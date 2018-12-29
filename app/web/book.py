from flask import request, render_template
from flask_login import current_user
from app.forms.book import SearchForm
from app.libs.helper import *
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.web import web

__author__ = "TuDi"
__date__ = "2018/12/17 下午2:59"


@web.route("/book/search/")
def search():
    # q = "9787101056365"
    form = SearchForm(request.args)
    books = YuShuBook()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == "key":
            books.search_by_keyword(q, page)
        if isbn_or_key == "isbn":
            books.search_by_isbn(q)
            # return json.dumps(result), 200, {"content-type": "application/json"}
            # return json.dumps(result, default=lambda o: o.__dict__)
    # return render_template("test.html", data={"a": "", "b": 2})
    return render_template("search_result.html", books=books, form=form)


@web.route("/book/<isbn>/detail/")
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()

    book = YuShuBook()
    book.search_by_isbn(isbn)
    return render_template("book_detail.html", book=book.first, has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes, wishes=trade_wishes, gifts=trade_gifts,
                           wishs_len=len(trade_wishes), gifts_len=len(trade_gifts))
