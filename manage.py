from app import app

__author__ = "TuDi"
__date__ = "2018/12/15 上午12:58"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=app.config["DEBUG"])
