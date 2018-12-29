from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from contextlib import contextmanager
from flask_mail import Mail

__author__ = "TuDi"
__date__ = "2018/12/17 下午6:32"

# 实例化 Flask
app = Flask(__name__)

# 加载配置文件
app.config.from_object("app.secure")
app.config.from_object("app.setting")



class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if "status" not in kwargs.keys():
            kwargs["status"] = 1
        return super().filter_by(**kwargs)

# 注册 SQLAlchemy
db = SQLAlchemy(app, query_class=Query)

# 注册用户登录管理插件 LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "web.login"
login_manager.login_message = "请先登录或注册"

# 注册发送邮件插件 Mail
mail = Mail(app)

# 注册 web 蓝图
from app.web import web

app.register_blueprint(web)



