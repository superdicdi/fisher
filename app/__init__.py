from flask import Flask
from app.web import web
from flask_sqlalchemy import SQLAlchemy

__author__ = "TuDi"
__date__ = "2018/12/17 下午6:32"

# 实例化 Flask
app = Flask(__name__)

# 加载配置文件
app.config.from_object("app.secure")
app.config.from_object("app.setting")

# 注册 SQLAlchemy
db = SQLAlchemy(app)

# 注册 web 蓝图
app.register_blueprint(web)
