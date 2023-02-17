HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'skyrimlight'
PASSWORD = 'skyrimlight'
DATABASE = 'flask'
DB_URL = F'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DB_URL
# DB_URI = 'mysql+pymysql://skyrimlight:skyrimlight@127.0.0.1:3306/python'
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

SECRET_KEY = 'skyrimlight'
BASE_DIR = r'C:\Users\10708\Desktop\认识python\web项目\flaskBlog'
