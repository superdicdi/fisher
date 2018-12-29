from flask import Blueprint, render_template

__author__ = "TuDi"
__date__ = "2018/12/17 下午6:32"

web = Blueprint("web", __name__)


@web.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
