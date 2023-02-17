from enum import IntEnum

from flaskBlog.exts import db
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True
    add_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class Category(BaseModel):
    """分类模型"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    icon = db.Column(db.String(128), nullable=True)
    post = db.relationship('Post', backref='category', lazy=True)

    # 分类管理的级联删除
    # post = db.relationship('Post', back_populates='category', cascade='all,delete', passive_deletes=True,)

    def __repr__(self):
        return '<Category %r>' % self.name


# 多对多关系帮助器表
tags = db.Table('tags', db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True))


class PostPublishType(IntEnum):
    """ 文章发布类型
    """
    draft = 1  # 草稿
    show = 2  # 发布


class Post(BaseModel):
    """文章模型"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(255), nullable=True)
    has_type = db.Column(db.Enum(PostPublishType), server_default='show', nullable=False)
    content = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ), nullable=False)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('post', lazy=True))

    # comment = db.relationship('Comment', back_populates='post', cascade='all,delete', passive_deletes=True)

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(BaseModel):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return self.name


class Blog_User(BaseModel):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(320), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    is_super_user = db.Column(db.Boolean, nullable=True, default=False)
    is_active = db.Column(db.Boolean, nullable=True, default=True)
    is_staff = db.Column(db.Boolean, nullable=True, default=False)
    signature = db.Column(db.String(100), nullable=True)
    desc = db.Column(db.String(150), nullable=True)
    gender = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)

    # comment = db.relationship('Comment', backref='user', lazy='True')

    def __repr__(self):
        return '<Category %r>' % self.username


class Banner(BaseModel):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    url = db.Column(db.String(300), nullable=True)

    # def __repr__(self):
    # return f'{self.id}=>{self.img}+{self.url}'
    # return f'{self.img}, {self.url}'


class Comment(BaseModel):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(200), nullable=True)
    # post = db.relationship('Post', db.ForeignKey('post.id'))
    user = db.relationship('Blog_User', backref='comment')
    post = db.relationship('Post', backref='comment')
    # user = db.relationship('Blog_User')
    user_id = db.Column(db.Integer, db.ForeignKey(Blog_User.id, ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    # post = db.relationship('Post', back_populates='comment')

    # 　　posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return self.content
