from flask import Flask
from flask_login import LoginManager
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

# 注册用户登录管理插件 LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "web.login"
login_manager.login_message = "请先登录或注册"
# 注册 web 蓝图
from app.web import web
app.register_blueprint(web)
