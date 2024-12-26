from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import pymysql
pymysql.install_as_MySQLdb()
load_dotenv()

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Kiểm tra biến môi trường
    if not os.getenv('DATABASE_URL') or not os.getenv('MAIL_USERNAME') or not os.getenv('MAIL_PASSWORD'):
        raise ValueError("Cần phải cung cấp DATABASE_URL và các thông tin email trong tệp .env")

    # Cấu hình cơ sở dữ liệu
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Cấu hình ứng dụng cho Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    mail.init_app(app)

    # Đăng ký blueprint
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/')

    return app
