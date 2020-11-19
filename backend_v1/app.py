# app
from flask import Flask, abort, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__, template_folder="template", static_folder="resource")
CORS(app, supports_credentials=True)
# @app.after_request
# def after_request(resp):
# 	resp = make_response(resp)
# 	resp.headers['Access-Control-Allow-Origin'] = '*'
# 	resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
# 	resp.headers['Access-Control-Allow-Headers'] = 'content-type,token'
# 	return resp

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/curious_v1"

# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
app.config['SQLALCHEMY_TRACK_MODEIFICATIONS'] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 1000

# 实例化db对象
db = SQLAlchemy(app)

# # 定义错误页面404.500
# @app.errorhandler(404)
# def page_not_fo und(e):
#     return render_template('error_404.html')


if __name__ == '__main__':
    from controller.index import *
    app.register_blueprint(index)

    from controller.user import *
    app.register_blueprint(user)

    from controller.question import *
    app.register_blueprint(question)

    from controller.answer import *
    app.register_blueprint(answer)

    from controller.collection import *
    app.register_blueprint(collection)

    from controller.history import *
    app.register_blueprint(history)

    from controller.upvote import *
    app.register_blueprint(upvote)

    from controller.notification import *
    app.register_blueprint(notification)

    from controller.recommend import *
    app.register_blueprint(recommend)

    from controller.admin import *
    app.register_blueprint(admin)




    app.run(debug=True)
