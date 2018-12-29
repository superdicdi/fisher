__author__ = "TuDi"
__date__ = "2018/12/16 上午12:27"

DEBUG = True
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/fisher?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "123456"


# Email 配置
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'superdi_cdi@163.com'
MAIL_PASSWORD = 'tudi7208562'
MAIL_DEFAULT_SENDER = 'superdi_cdi@163.com'
