import functools

from flask import request, render_template, Blueprint, session, redirect, url_for, flash, g
from flaskBlog.models import Blog_User, Comment, Post
from flaskBlog.until.get_md5 import get_md5
from flaskBlog.exts import db
from flaskBlog.utils import upload_file_path
from flaskBlog.views.forms import LoginForm, RegisterForm, CreateUserForm

au = Blueprint('auth', __name__, url_prefix='/user')


@au.before_app_request
def load_login_in_user():  # put application's code here
    user_id = session.get('id')
    urls = ['user', 'blog']
    # print(request.path)
    request_url_path = request.path.split('/')
    if request_url_path[0] == '':
        request_url = request_url_path[1]
    else:
        request_url = request_url_path[0]
    # print('++++', request_url_path)
    print(request_url_path)
    print(request_url)
    if user_id:
        g.user = Blog_User.query.filter_by(id=user_id).first()
        if g.user and g.user.is_super_user and g.user.is_active:
            g.user.has_perm = 1
        elif not g.user.is_super_user and g.user.is_active and not g.user.is_staff and request_url in urls:
            # elif g.user and request.path in urls:
            # elif request.path in urls:
            g.user.has_perm = 1
        else:
            g.user.has_perm = 0
    else:
        g.user = None


def login_required(view):
    @functools.wraps(view)
    def inner(*args, **kwargs):
        if g.user is None:
            redirect_to = f"{url_for('auth.login')}?redirect_to={request.path}"
            return redirect(redirect_to)
        if not g.user.has_perm:
            return '<h1>无权限查看</h1>'

        return view(*args, **kwargs)

    return inner


@au.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    redirect_to = request.args.get('redirect_to')
    form = LoginForm()
    if form.validate_on_submit():
        user = Blog_User.query.filter_by(username=form.username.data).first()
        session.clear()
        session['id'] = user.id
        if redirect_to is not None:
            return redirect(redirect_to)
        return redirect(url_for('blog.index'))
    return render_template('login.html', form=form)
    # session_id = session.get('id')
    # if request.method == 'GET':
    #     if not session_id:
    #         return render_template('login.html')
    #     else:
    #         return render_template('index.html')
    #
    # form_data = request.form
    # username = form_data.get('username')
    # password = get_md5(form_data.get('password'))
    # # print(password)  # 18247614e12132453d814ceb480d263b
    # user_info = Blog_User.query.filter_by(username=username, password=password).first()
    # if user_info:
    #     session['id'] = user_info.id
    #     # print('登陆成功')
    #     return redirect(url_for('blog.index'))
    # else:
    #     flash('用户名或密码错误')
    #     return render_template('login.html', errors='用户名或密码错误')


@au.route('/register', methods=['GET', 'POST'])
def register():  # put application's code here
    # data_info = {}
    # if request.method == 'GET':
    #     return render_template('register.html', data_info=data_info)
    # form = request.form
    # username = form.get('username')
    # password = form.get('password')
    # password_conf = form.get('password_conf')
    # data_info = {'username': username, 'password': password, 'password_conf': password_conf}
    # if password_conf != password:
    #     data_info['pasword_error'] = '两次输入的密码不一致'
    #     flash('两次输入的密码不一致')
    #     return render_template('register.html', data_info=data_info)
    # user_conf = Blog_User.query.filter_by(username=username).first()
    # if user_conf:
    #     data_info['user_error'] = '用户已注册'
    #     flash('用户已注册')
    #     return render_template('register.html', data_info=data_info)
    # else:
    #     password = get_md5(password)
    #     data_info = Blog_User(username=username, password=password)
    #     db.session.add(data_info)
    #     db.session.commit()
    #     session.clear()
    #     session['id'] = data_info.id
    #     return redirect(url_for('login'))
    # form = RegisterForm()
    form = RegisterForm(request.form)
    # print(request.form.password.data)
    datainfo = request.form
    if form.validate():
        # if form.validate_on_submit():
        user = Blog_User(username=form.username.data, password=get_md5(form.password.data))
        db.session.add(user)
        db.session.commit()
        session.clear()
        session['id'] = user.id
        return redirect(url_for('blog.index'))
    data_form = request.form
    username = data_form.get('username')
    password = data_form.get('password')
    password_conf = data_form.get('password_conf')
    data_info = {'username': username, 'password': password, 'password_conf': password_conf}
    return render_template('register.html', data_info=data_info, form=form)


@au.route('/logout', methods=['GET', 'POST'])
def logout():  # put application's code here
    session.clear()
    return redirect(url_for('auth.login'))


@au.route('/')
@login_required
def userinfo():
    return render_template('userinfo.html')


@au.route('/user_comments')
@login_required
def user_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(user_id=g.user.id).order_by(-Comment.add_date).paginate(page=page, per_page=5)
    comment_list = pagination.items
    print(comment_list)

    return render_template('user_comments.html', pagination=pagination, comment_list=comment_list)


@au.route('/comment_post/<comment_id>')
@login_required
def comment_post(comment_id):
    comment_info = Comment.query.get(comment_id)
    post_id = comment_info.post_id
    post_info = Post.query.get(post_id)
    cate_id = post_info.category_id
    # return redirect(url_for(f'blog.detail.{post_id}'))
    return redirect(url_for(f'blog.detail', post_id=post_id, cate_id=cate_id))


@au.route('/comment_del/<comment_id>')
@login_required
def comment_del(comment_id):
    comment_info = Comment.query.get(comment_id)
    db.session.delete(comment_info)
    db.session.commit()
    flash(f'删除成功')
    return redirect(url_for('admin.comment'))


@au.route('/user_edit', methods=['POST', 'GET'])
@login_required
def user_edit():
    user_info = Blog_User.query.get(g.user.id)
    form = CreateUserForm(username=user_info.username, password='', is_super_user=user_info.is_super_user,
                          is_staff=user_info.is_staff, is_active=user_info.is_active, avatar=user_info.avatar,
                          signature=user_info.signature, desc=user_info.desc, gender=user_info.gender,
                          address=user_info.address, email=user_info.email)
    if form.validate_on_submit():
        user_info.username = g.user.username
        if form.password.data != '':
            user_info.password = get_md5(form.password.data)
            session.clear()
        # user_info.is_super_user = form.is_super_user.data
        # user_info.is_active = form.is_active.data
        # user_info.is_staff = form.is_staff.data
        # user_info.avatar = form.avatar.data
        f = form.avatar.data
        if user_info.avatar == f:
            user_info.avatar == user_info.avatar
        else:
            avatar_path, filename = upload_file_path('avatar', f)
            user_info.avatar = f'avatar/{filename}'
            f.save(avatar_path)
        user_info.gender = form.gender.data
        user_info.signature = form.signature.data
        user_info.desc = form.desc.data
        user_info.address = form.address.data
        user_info.email = form.email.data

        db.session.add(user_info)
        db.session.commit()
        flash(f'修改成功')
        return redirect(url_for('auth.userinfo'))
    return render_template('user_user_form.html', form=form, user_info=user_info)
