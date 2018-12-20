from flask import Blueprint

__author__ = "TuDi"
__date__ = "2018/12/17 下午6:32"

web = Blueprint("wed", __name__)
from app.web import book
