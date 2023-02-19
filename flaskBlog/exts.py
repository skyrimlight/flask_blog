# 这个文件存在的目的就是为了解决循环应用的问题
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache


db = SQLAlchemy()
cache = Cache()
