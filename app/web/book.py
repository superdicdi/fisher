import json

from flask import jsonify, request, render_template, flash

from app.forms.book import SearchForm
from app.libs.helper import *
from app.spider.yushu_book import YuShuBook
from app.web import web

__author__ = "TuDi"
__date__ = "2018/12/17 下午2:59"


@web.route("/book/search")
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
    print("aa")
    return render_template("search_result.html", books=books, form=form)


@web.route("/book_detail/")
def book_detail():
    pass


