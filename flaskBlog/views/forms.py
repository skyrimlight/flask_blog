from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SelectMultipleField, RadioField, FileField, \
    BooleanField, EmailField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from werkzeug.security import check_password_hash

from flaskBlog.models import Blog_User, PostPublishType
from flaskBlog.until.get_md5 import get_md5


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(message='不能为空'),
        Length(max=32, message='用户名过长')
        # ], filters=(qs_username,))
    ])
    password = StringField('password', validators=[
        DataRequired(message='不能为空'),
        Length(max=32, message='密码长度不能超过32位')
    ])

    # 自定义验证内容
    def validate_username(form, field):
        user_info = Blog_User.query.filter_by(username=field.data, password=get_md5(form.password.data)).first()
        if not user_info:
            error = '用户名或密码错误'
            # print('登陆成功')
            raise ValidationError(error)


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(message='不能为空'),
        Length(max=32, message='用户名过长')
        # ], filters=(qs_username,))
    ])
    password = PasswordField('password', validators=[
        DataRequired(message='不能为空'),
        Length(min=8, max=32, message='密码长度不能超过32位'),
        EqualTo('password_conf', message='两次输入的密码不一致')
    ])
    password_conf = PasswordField('password_conf')

    def validate_username(form, field):
        user_info = Blog_User.query.filter_by(username=field.data).first()
        if user_info:
            error = '用户已经存在'
            # print('登陆成功')
            raise ValidationError(error)


class CategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[
        DataRequired(message='不能为空'), Length(max=128, message='不符合字数要求')
    ])
    icon = StringField('分类图标', validators=[
        Length(max=128, message='不符合长度要求')
    ])


class PostForm(FlaskForm):
    title = StringField("文章标题", validators=[
        DataRequired(message='内容不能为空'), Length(max=128, message='不符合字数要求')
    ])
    desc = StringField('文章描述', validators=[DataRequired(message="不能为空"),
                                               Length(max=255, message='不符合字数要求')
                                               ])
    category_id = SelectField(
        '分类',
        choices=None,
        coerce=int,
        validators=[
            DataRequired(message="不能为空"),
        ]
    )
    content = TextAreaField('文章详情',
                            validators=[DataRequired(message="不能为空")]
                            )
    has_type = RadioField('发布状态',
                          choices=(PostPublishType.draft.name, PostPublishType.show.name),
                          default=PostPublishType.show.name)
    tags = SelectMultipleField('文章标签', choices=None, coerce=int)


class TagForm(FlaskForm):
    name = StringField('标签名称', validators=[Length(max=255, message='超出长度')])


class Blog_UserForm(FlaskForm):
    avatar = FileField('用户头像', Length(max=200))

    # username = db.Column(db.String(128), nullable=False, unique=True)
    # password = db.Column(db.String(320), nullable=False)
    # avatar = db.Column(db.String(200), nullable=True)


from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed


class CreateUserForm(FlaskForm):
    # 创建表单
    username = StringField('用户名', validators=[
        DataRequired(message="不能为空"),
        Length(max=32, message="不符合字数要求！")
    ])
    password = PasswordField('密码', validators=[
        # DataRequired(message="不能为空"),
        Length(max=32, message="不符合字数要求！")
    ], description="修改用户信息时，留空则代表不修改！")
    avatar = FileField("头像", validators=[
        # FileRequired(),
        FileAllowed(['jpg', 'png', 'gif'], message="仅支持jpg/png/gif格式"),
        FileSize(max_size=2048000, message="不能大于2M")],
                       description="大小不超过2M，仅支持jpg/png/gif格式，不选择则代表不修改")
    is_super_user = BooleanField("是否为管理员")
    is_active = BooleanField("是否活跃", default=True)
    is_staff = BooleanField("是否锁定")
    desc = StringField('简介', validators=[
        Length(max=150, message="不符合字数要求！")
    ])
    gender = SelectField('性别', choices=(('man', '男'), ('woman', '女')))
    email = EmailField('邮箱', )
    address = StringField('地址', validators=[Length(max=150, message="不符合字数要求！")])
    signature = StringField('个性签名', validators=[Length(max=100, message="不符合字数要求！")])
    # signature = db.Column(db.String(100), nullable=True)


class BannerForm(FlaskForm):
    img = FileField("轮播图片", validators=[
        FileAllowed(['jpg', 'png', 'gif'], message="仅支持jpg/png/gif格式"),
        FileSize(max_size=2048000, message="不能大于2M")],
                    description="大小不超过2M，仅支持jpg/png/gif格式，不选择则代表不修改")
    desc = StringField('图片描述', validators=[
        Length(max=200, message='超过描述长度')
    ])
    url = StringField('图片地址', validators=[
        Length(max=200, message='超过描述长度')
    ])


class CommentForm(FlaskForm):
    # 分类表单
    content = TextAreaField('分类名称', validators=[
        DataRequired(message='不能为空'),
        Length(max=200, message='字数超出限制')
    ])
