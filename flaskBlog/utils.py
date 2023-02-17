import os
import uuid

from werkzeug.utils import secure_filename

# # #
# # #
# # # def update_filename(f):
# # #     # 修改文件名
# # #     names = list(os.path.splitext(secure_filename(f.filename)))
# # #     names[0] = "".join(str(uuid.uuid4()).split('-'))
# # #     return "".join(names)
# # #
# # #
# # # # path = '/static/img/avatar'
# # #
# # #
# # # def save_avatar(path, f):
# # #     file_path = os.path.abspath(path)
# # #     file_name = update_filename(f)
# # #     return file_path / file_name, file_name
# # import os
# # import uuid
# # # from flaskBlog.config import BASE_DIR
# # from werkzeug.utils import secure_filename
# #
# #
# # #
# # # def _file_path(directory_name):
# # #     """判断该路径是否存在不存在则创建
# # #     """
# # #     file_path = f'flaskBlog/static/{directory_name}'
# # #     if os.path.exists(file_path) is False:
# # #         os.makedirs(file_path)
# # #     return file_path
# # #
# # #
# # def update_filename(f):
# #     """修改文件名
# #     """
# #     names = list(os.path.splitext(secure_filename(f)))
# #     names[0] = ''.join(str(uuid.uuid4()).split('-'))
# #     img_name = ''.join(names)
# #     with open(r'C:\Users\10708\Desktop\认识python\web项目\flaskBlog\static\img\avatar' + img_name, 'wb') as file:
# #         file.write(f)
# #     return img_name
# #
# # #
# # #
# # # def upload_file_path(directory_name, f):
# # #     # 构造上传文件路径
# # #     file_path = _file_path(directory_name)
# # #     filename = update_filename(f)
# # #     return file_path / filename, filename
# #
# #
# # # def save_file(f):
# # #     file_path = r'C:\Users\10708\Desktop\认识python\web项目\flaskBlog\static\img\avatar'
# # #     filename = update_filename(f)
#
# import os
# import uuid
# from flaskBlog.config.settings import BASE_DIR
# from werkzeug.utils import secure_filename
#
#
# def _file_path(directory_name):
#     """判断该路径是否存在不存在则创建
#     """
#     # file_path = BASE_DIR + f'/static/{directory_name}'
#     file_path = r'C:\Users\10708\Desktop\认识python\web项目\flaskBlog\static\avatar'
#
#     if os.path.exists(file_path) is False:
#         os.makedirs(file_path)
#     return file_path
#
#
# def update_filename(f):
#     """修改文件名
#     """
#     names = list(os.path.splitext(secure_filename(f.filename)))
#     names[0] = ''.join(str(uuid.uuid4()).split('-'))
#     return ''.join(names)
#
#
# def upload_file_path(directory_name, f):
#     # 构造上传文件路径
#     file_path = _file_path(directory_name)
#     filename = update_filename(f)
#     return file_path / filename, filename

# def upload_file_path(f):
#     # 构造上传文件路径
#     file_path = r'static\avatar'
#     # print(os.path.basename(f))
#     # filename = str(uuid.uuid4) + os.path.basename(f)
#
#     return file_path
import os
import uuid
# from RealProject.config import BASE_DIR
from werkzeug.utils import secure_filename
from datetime import datetime
import time

BASE_DIR = 'static/img/avatar'


def _file_path(directory_name):
    """判断该路径是否存在不存在则创建
    """
    file_path = f'C:/Users/10708/Desktop/认识python/web项目/flaskBlog/static/img/{directory_name}'
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    return file_path


def update_filename(f):
    """修改文件名
    """
    names = list(os.path.splitext(secure_filename(f.filename)))
    names[0] = ''.join(str(uuid.uuid4()).split('-'))
    return ''.join(names)


def upload_file_path(directory_name, f):
    # 构造上传文件路径
    file_path = _file_path(directory_name)
    filename = update_filename(f)
    return file_path + '/' + filename, filename
