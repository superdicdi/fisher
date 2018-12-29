import os

from werkzeug.local import LocalStack

__author__ = "TuDi"
__date__ = "2018/12/18 下午5:25"

from flask import Flask, current_app
import threading
# app = Flask(__name__)
# cxt = app.app_context()
# cxt.push()
# a = current_app
# pass

# local = LocalStack()
# local.push(1)
# local.push(2)
#
# print("first", local.top)
# def work():
#     print("two", local.top)
#     local.push(3)
#     local.push(4)
#     print("three", local.top)
#
# t = threading.Thread(target=work)
# t.start()
#
# print("four", local.top)
a = [{'name':'Andy','age':25},{'name':'Joe','age':40},
	{'name':'Ken','age':16},{'name':'Julia','age':31}
]
# b =sorted(a, key=lambda x : x["age"])
# print(b)
print(type(a))
a.sort(key=lambda x : x["age"])

print(a)
print(type(a))
