from flask import request, render_template, Blueprint, session, redirect, url_for, g, flash
import random
from flaskBlog.exts import db
from flaskBlog.models import Blog_User, Post, Category, Tag, Comment, Banner
from flaskBlog.views.auth import login_required
from flaskBlog.views.forms import CommentForm
import requests

bg = Blueprint('blog', __name__, url_prefix='/blog')


@bg.route('/index')
def index():  # put application's code here
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(page=page, per_page=3)
    post_list = pagination.items
    # post_list = [1, 2, 3, 4, 5, 6]
    imgs = [
        'https://th.bing.com/th/id/R.d8dfd08893b58d08d74b38ad8870a48d?rik=FOH776EhG01I%2bA&riu=http%3a%2f%2fstatic.cntonan.com%2fuploadfile%2f2020%2f0318%2f20200318122901txdvkwgvpsw.jpg&ehk=2OKIaIz3xTccGgjf5DFKNDfJLcPfvXjuF%2bJbC6GJk6w%3d&risl=&pid=ImgRaw&r=0',
        'https://th.bing.com/th/id/R.466bb61cd7cf4e8b7d9cdf645add1d6e?rik=YRZKRLNWLutoZA&riu=http%3a%2f%2f222.186.12.239%3a10010%2fwmxs_161205%2f002.jpg&ehk=WEy01YhyfNzzQNe1oIqxwgbTnzY7dMfmZZHkqpZB5WI%3d&risl=&pid=ImgRaw&r=0',
        'https://th.bing.com/th/id/R.987f582c510be58755c4933cda68d525?rik=C0D21hJDYvXosw&riu=http%3a%2f%2fimg.pconline.com.cn%2fimages%2fupload%2fupc%2ftx%2fwallpaper%2f1305%2f16%2fc4%2f20990657_1368686545122.jpg&ehk=netN2qzcCVS4ALUQfDOwxAwFcy41oxC%2b0xTFvOYy5ds%3d&risl=&pid=ImgRaw&r=0']
    for post in post_list:
        post.img = random.sample(imgs, 1)[0]
    # path = r'C:\Users\10708\Desktop\认识python\web项目\flaskBlog\static\img\daily.jpg'
    # import os
    # if not os.path.exists(path):
    #     import re
    #     url = 'https://www.bing.com'
    #     headers = {
    #         "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    #     }
    #     data = requests.get(url, headers=headers)
    #     # print(data.text.encode('utf-8'))
    #     urls = re.search(string=data.content, pattern=b'(/th\?id=OHR.+?\.jpg)')
    #     # print(url + urls.group().decode('utf-8'))
    #     img_url = url + urls.group().decode('utf-8')
    #     img = requests.get(img_url, headers=headers)
    #     data = img.content
    #     with open(path, 'wb') as f:
    #         f.write(data)
    img_url = Banner.query.all()
    # img_list = img_list[1:3]
    # img_first = Banner.query.order_by(-Banner.add_date).first()
    # print(img_info)
    # img_list = []
    # for i in img_info.img:
    #     if i and i not in [1, '1']:
    #         img_list.append('img' + img_info.img)
    #     else:
    #         img_list.append(img_info.url)
    # print(img_list)
    # img_url_list = img_url.split(',')
    # img_list=[]
    # for i in range(0,6,2):
    #     if i == '1':
    #         img_list.append()
    # print(img_url[0].img)
    # print(img_list.items())
    # print(img_list[2])
    img_first = img_url[0]
    img_list = img_url[1:]
    return render_template('index.html', pagination=pagination, post_list=post_list, img_list=img_list,
                           img_first=img_first)


@bg.route('/category/<int:cate_id>')
@login_required
def cates(cate_id):
    # 分类页
    cate = Category.query.get(cate_id)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.category_id == cate_id).paginate(page=page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template('cate_list.html', cate=cate, post_list=post_list, cate_id=cate_id, pagination=pagination)


@bg.route('/details/<int:cate_id>/<int:post_id>', methods=['GET', 'POST'])
@login_required
def detail(cate_id, post_id):
    cate = Category.query.get(cate_id)
    post = Post.query.get_or_404(post_id)
    # 上一篇
    prev_post = Post.query.filter(Post.id < post_id).order_by(-Post.id).first()
    # 下一篇
    next_post = Post.query.filter(Post.id > post_id).order_by(Post.id).first()

    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter(Comment.post_id == post.id).order_by(-Comment.add_date).paginate(page=page,
                                                                                                       per_page=5)
    comment_list = pagination.items

    # 评论功能
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data,
                          post_id=post.id, user_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        flash('评论成功')
        return redirect(f"{url_for('blog.detail', cate_id=cate_id, post_id=post_id)}#comment")

    return render_template('detail.html', cate=cate, post=post, prev_post=prev_post, next_post=next_post,
                           comment_list=comment_list, pagination=pagination, form=form)


@bg.context_processor
def inject_archive():
    # 文章归档日期注入上下文
    posts = Post.query.order_by(Post.add_date)
    dates = set([post.add_date.strftime("%Y年%m月") for post in posts])
    tags = Tag.query.all()
    for tag in tags:
        tag.style = ['is-success', 'is-danger', 'is-black', 'is-light', 'is-primary', 'is-link', 'is-info',
                     'is-warning']
    new_posts = posts.limit(3)
    return dict(dates=dates, tags=tags, new_posts=new_posts)


@bg.route('/category/<string:date>')
@login_required
def archive(date):
    import re
    # regex = re.compile(r'(\d{4})\s+(\d{2})')
    # print(date)
    # dates = re.findall(string=date, pattern=r'\d{4}\s+\d{2}')  # ['2023','02']
    # dates = [date[:4], date[5:7]]
    dates = re.findall(string=date, pattern=r'(\d{4})\w+(\d{2})')
    from sqlalchemy import extract, and_, or_
    archive_posts = Post.query.filter(
        and_(extract('year', Post.add_date) == int(dates[0][0]),
             extract('month', Post.add_date) == int(dates[0][1])
             ))
    # 对数据进行分页
    page = request.args.get('page', 1, type=int)
    pagination = archive_posts.paginate(page=page, per_page=5, error_out=False)
    return render_template('archive.html', post_list=pagination.items, pagination=pagination, date=date)


@bg.route('/tags/<tag_id>')
@login_required
def tags(tag_id):
    # tags_post = Post.query.filter(Tag.id == tag_id).order_by(-Post.add_date).limit(6)
    tag = Tag.query.get(tag_id)
    return render_template('tags.html', post_list=tag.post, tag=tag)
    # page = request.args.get('page', 1, type=int)
    # pagination = tags_post.paginate(page=page, per_page=5, error_out=False)
    # return render_template('tags.html', post_list=pagination.items, pagination=pagination, tags_post=tags_post)
    #
    # pass


@bg.route('/search')
@login_required
def search():
    words = request.args.get('words', type=str)
    data = Post.query.filter(Post.title.like('%' + words + '%')).order_by(-Post.add_date)
    page = request.args.get('page', 1, type=int)
    pagination = data.paginate(page=page, per_page=5, error_out=False)
    post_list = pagination.items
    return render_template('search.html', page=page, pagination=pagination, post_list=post_list, words=words)
