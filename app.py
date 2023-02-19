import requests
from flask import Flask, render_template, request, redirect, g
from flask_migrate import Migrate
from flaskBlog.config import settings
import redis
from flask_caching import Cache
from flaskBlog.exts import cache
from flaskBlog.models import *
from flaskBlog.views.blog import bg as bg_bp
from flaskBlog.views.auth import au as au_bp
from flaskBlog.views.admin import admin as admin_bp
from flaskBlog.views import blog
import requests

config = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': '127.0.0.1',
    'CACHE_REDIS_PORT': 6379

}

app = Flask(__name__)
app.config.from_object(settings)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(au_bp)
app.register_blueprint(bg_bp)
app.register_blueprint(admin_bp)

app.add_url_rule('/', endpoint='index', view_func=blog.index)

# 初始化缓存文件
cache.__init__(app=app, config=config)

# app.register_blueprint(auth_bp)


# @app.route('/')
# def hello_world():  # put application's code here
#
#     return render_template('index.html')


from flaskBlog.models import Category


def inject_category():
    categorys = Category.query.limit(6).all()
    return dict(categorys=categorys)


app.context_processor(inject_category)
if __name__ == '__main__':
    app.run()
