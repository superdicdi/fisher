import json

from flask import jsonify, request

from app.forms.book import SearchForm
from app.libs.helper import *
from app.spider.yushu_book import YuShuBook
from app.web import web
from app.view_models.book import BookViewModels

__author__ = "TuDi"
__date__ = "2018/12/17 下午2:59"
from flask import _request_ctx_stack

@web.route("/book/search")
def search():
    # q = "9787101056365"
    form = SearchForm(request.args)
    if form.validate():
        result = ""
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        result = YuShuBook()
        if isbn_or_key == "key":
            result.search_by_keyword(q, page)
        if isbn_or_key == "isbn":
            result.search_by_isbn(q)
        # return json.dumps(result), 200, {"content-type": "application/json"}
        return json.dumps(result, default=lambda o: o.__dict__)
    else:
        return jsonify({})
