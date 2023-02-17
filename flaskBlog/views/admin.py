from flask import Flask, Blueprint, render_template, url_for, g, request, redirect, flash
from flask_sqlalchemy import pagination
from flaskBlog.exts import db
from flaskBlog.until.get_md5 import get_md5
from flaskBlog.views.auth import login_required

from flaskBlog.models import Category, Post, Tag, Blog_User, Banner, Comment
from flaskBlog.views.forms import CategoryForm, PostForm, TagForm, CreateUserForm, BannerForm
# from flaskBlog.utils import save_avatar,update_filename
from flaskBlog.utils import upload_file_path
from datetime import datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
def index():
    posts_all = Post.query.count()
    user_all = Blog_User.query.count()
    comments_all = Comment.query.count()
    return render_template('admin_index.html', posts_all=posts_all, user_all=user_all, comments_all=comments_all)
    # posts_all = Post.query.all().count()
    # user_all = Blog_User.query.all().count()
    # return render_template('admin_index.html')


@admin.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    # category_data = Category(name='flask')
    # db.session.add(category_data)
    # db.session.commit()
    if request.method == 'GET':
        form = CategoryForm()
        page = request.args.get('page', 1, type=int)
        # print(page)
        pagination = Category.query.order_by(-Category.add_date).paginate(page=page, per_page=2)
        category_list = pagination.items

        return render_template('category.html', category_list=category_list, pagination=pagination)


@admin.route('/category/add', methods=['POST', 'GET'])
@login_required
def category_add():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, icon=form.icon.data)
        db.session.add(category)
        db.session.commit()
        flash(f'{form.name.data}分类添加成功')
        return redirect(url_for('admin.category'))
    return render_template('category_form.html', form=form)


@admin.route('/category/edit/<nid>', methods=['POST', 'GET'])
@login_required
def category_edit(nid):
    # nid = request.args.get('nid')
    edit_info = Category.query.get(nid)
    form = CategoryForm(name=edit_info.name, icon=edit_info.icon)
    if request.method == 'GET':
        return render_template('category_form.html', form=form)
    if form.validate_on_submit():
        # category = Category(name=form.name.data, icon=form.icon.data)
        edit_info.name = form.name.data
        edit_info.icon = form.icon.data
        db.session.add(edit_info)
        db.session.commit()
        flash(f'{form.name.data}分类修改成功')
        return redirect(url_for('admin.category'))
    return render_template('category_form.html', form=form)


@admin.route('/category/delete/<nid>', methods=['GET'])
@login_required
def category_delete(nid):
    delete_info = Category.query.get(nid)
    if delete_info:
        # 级联删除
        Post.query.filter(Post.category_id == delete_info.id).delete()
    db.session.delete(delete_info)
    db.session.commit()
    flash(f'分类删除成功')
    return redirect(url_for('admin.category'))


@admin.route('/article', methods=['GET', 'POST'])
@login_required
def article():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(page=page, per_page=2)
    post_list = pagination.items

    return render_template('article.html', post_list=post_list, pagination=pagination)


@admin.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
    form = PostForm()
    form.category_id.choices = [(i.id, i.name) for i in Category.query.all()]
    form.tags.choices = [(i.id, i.name) for i in Tag.query.all()]
    # page = request.args.get('page', 1, type=int)
    # pagination = Post.query.order_by(-Post.add_date).paginate(page=page, per_page=2)
    # post_list = pagination.items
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    desc=form.desc.data,
                    has_type=form.has_type.data,
                    content=form.content.data,
                    category_id=int(form.category_id.data)
                    )
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}分类添加成功')
        return redirect(url_for('admin.article'))

    return render_template('article_form.html', form=form)


@admin.route('/article_edit/<nid>', methods=['GET', 'POST'])
@login_required
def article_edit(nid):
    edit_data = Post.query.get(nid)
    tags = [i.id for i in edit_data.tags]
    form = PostForm(title=edit_data.title, desc=edit_data.desc, content=edit_data.content,
                    has_type=edit_data.has_type.value, tags=tags)
    form.category_id.choices = [(i.id, i.name) for i in Category.query.all()]
    form.tags.choices = [(i.id, i.name) for i in Tag.query.all()]
    if form.validate_on_submit():
        edit_data.title = form.title.data
        edit_data.desc = form.desc.data
        edit_data.has_type = form.has_type.data
        edit_data.content = form.content.data
        edit_data.category_id = int(form.category_id.data)
        edit_data.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        db.session.add(edit_data)
        db.session.commit()
        flash(f'{form.title.data}分类修改成功')
        return redirect(url_for('admin.article'))

    return render_template('article_form.html', form=form)


@admin.route('/article_delete/<nid>', methods=['GET', 'POST'])
@login_required
def article_delete(nid):
    edit_data = Post.query.get(nid)
    db.session.delete(edit_data)
    db.session.commit()
    flash(f'分类修改成功')
    return redirect(url_for('admin.article'))

    # return render_template('article_form.html', form=form)


@admin.route('/tag', methods=['GET', 'POST'])
@login_required
def tag():
    page = request.args.get('page', 1, type=int)
    pagination = Tag.query.order_by(-Tag.add_date).paginate(page=page, per_page=2)
    tag_list = pagination.items
    return render_template('tag.html', tag_list=tag_list, pagination=pagination)


@admin.route('/tag_add/', methods=['GET', 'POST'])
@login_required
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        tag_data = Tag(name=form.name.data)
        db.session.add(tag_data)
        db.session.commit()
        flash(f'{form.name.data}添加成功')
        return redirect(url_for('admin.tag'))
    return render_template('tag_form.html', form=form)


@admin.route('/tag_edit/<tag_id>', methods=['GET', 'POST'])
@login_required
def tag_edit(tag_id):
    tag_info = Tag.query.get(tag_id)
    form = TagForm(name=tag_info.name)
    if form.validate_on_submit():
        tag_info.name = form.name.data
        db.session.add(tag_info)
        db.session.commit()
        flash(f'{form.name.data}修改成功')
        return redirect(url_for('admin.tag'))
    return render_template('tag_form.html', form=form)


@admin.route('/tag_del/<tag_id>')
@login_required
def tag_del(tag_id):
    tag_info = Tag.query.get(tag_id)
    if tag_info:
        db.session.delete(tag_info)
        db.session.commit()
        return redirect(url_for('admin.tag'))


@admin.route('/user')
@login_required
def user():
    page = request.args.get('page', 1, type=int)
    pagination = Blog_User.query.order_by(-Blog_User.add_date).paginate(page=page, per_page=2)
    user_list = pagination.items
    return render_template('user.html', pagination=pagination, user_list=user_list)


@admin.route('/user_add', methods=['GET', 'POST'])
@login_required
def user_add():
    form = CreateUserForm()
    if form.validate_on_submit():
        f = form.avatar.data
        avatar_path, filename = upload_file_path('avatar', f)
        f.save(avatar_path)
        user = Blog_User(
            username=form.username.data,
            password=get_md5(form.password.data),
            avatar=f'avatar/{filename}',
            is_super_user=form.is_super_user.data,
            is_active=form.is_active.data,
            is_staff=form.is_staff.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'添加成功')
        return redirect(url_for('admin.user'))
    return render_template('user_form.html', form=form)

    # pass


@admin.route('/user_edit/<user_id>', methods=['POST', 'GET'])
@login_required
def user_edit(user_id):
    user_info = Blog_User.query.get(user_id)
    form = CreateUserForm(username=user_info.username, password='', is_super_user=user_info.is_super_user,
                          is_staff=user_info.is_staff, is_active=user_info.is_active, avatar=user_info.avatar)
    if form.validate_on_submit():
        user_info.username = form.username.data
        if user_info.password != '':
            user_info.password = get_md5(form.password.data)
        user_info.is_super_user = form.is_super_user.data
        user_info.is_active = form.is_active.data
        user_info.is_staff = form.is_staff.data
        # user_info.avatar = form.avatar.data
        f = form.avatar.data
        if user_info.avatar == f:
            user_info.avatar == user_info.avatar
        else:
            avatar_path, filename = upload_file_path('avatar', f)
            user_info.avatar = f'avatar/{filename}'
            f.save(avatar_path)
        db.session.add(user_info)
        db.session.commit()
        flash(f'修改成功')
        return redirect(url_for('admin.user'))
    return render_template('user_form.html', form=form, user_info=user_info)


@admin.route('/user_del/<user_id>')
@login_required
def user_del(user_id):
    user_info = Blog_User.query.get(user_id)
    db.session.delete(user_info)
    db.session.commit()
    return redirect(url_for('admin.user'))


@admin.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # 上传图片
    if request.method == 'POST':
        # 获取一个文件类型 request.files
        f = request.files.get('upload')
        file_size = len(f.read())
        f.seek(0)  # reset cursor position to beginning of file

        if file_size > 2048000:  # 限制上传大小为2M
            return {
                'code': 'err',
                'message': '文件超过限制2048000字节',
            }
        upload_path, filename = upload_file_path('upload', f)
        f.save(upload_path)
        return {
            'code': 'ok',
            'url': f'/admin/static/upload/{filename}'
        }


@admin.route('/img_change', methods=['GET', 'POST'])
@login_required
def img_change():
    page = request.args.get('page', 1, type=int)
    pagination = Banner.query.order_by(-Banner.add_date).paginate(page=page, per_page=5)
    img_list = pagination.items
    return render_template('img_change.html', pagination=pagination, img_list=img_list)


@admin.route('/img_add', methods=['GET', 'POST'])
@login_required
def img_add():
    form = BannerForm()
    if form.validate_on_submit():
        f = form.img.data
        if f:
            img_path, filename = upload_file_path('img', f)
            f.save(img_path)
            img = Banner(
                img=f'img/{filename}',
                desc=form.desc.data,
                url=form.url.data)
        else:
            img = Banner(
                img='1',
                desc=form.desc.data,
                url=form.url.data)
        db.session.add(img)
        db.session.commit()
        return redirect(url_for('admin.img_change'))
    return render_template('img_form.html', form=form)


@admin.route('/img_edit/<img_id>', methods=['GET', 'POST'])
@login_required
def img_edit(img_id):
    img_info = Banner.query.get(img_id)
    form = BannerForm(img=img_info.img, url=img_info.url, desc=img_info.desc)
    if form.validate_on_submit():
        f = form.img.data
        if f and f not in [1, '1']:
            img_path, filename = upload_file_path('img', f)
            f.save(img_path)
            img_info.img = f'img/{filename}'
            img_info.desc = form.desc.data
            img_info.url = form.url.data
        else:
            img_info.img = '1'
            img_info.desc = form.desc.data
            img_info.url = form.url.data
        db.session.add(img_info)
        db.session.commit()
        return redirect(url_for('admin.img_change'))
    return render_template('img_form.html', form=form)


@admin.route('/img_del/<img_id>', methods=['GET', 'POST'])
@login_required
def img_del(img_id):
    img_info = Banner.query.get(img_id)
    db.session.delete(img_info)
    db.session.commit()
    return redirect(url_for('admin.img_change'))


@admin.route('/comment')
@login_required
def comment():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(-Comment.add_date).paginate(page=page, per_page=5)
    comment_list = pagination.items
    return render_template('comment.html', pagination=pagination, comment_list=comment_list)


