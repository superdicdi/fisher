from flask import Blueprint

__author__ = "TuDi"
__date__ = "2018/12/17 下午6:32"

web = Blueprint("web", __name__)
from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
