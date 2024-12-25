from dotenv import load_dotenv
load_dotenv()  # Nạp các biến môi trường từ tệp .env

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Cấu hình cơ sở dữ liệu
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ebook.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://<username>:<password>@<host>/<database_name>')
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

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/')

    # from .routes_admin import api_admin
    # app.register_blueprint(api_admin, url_prefix='/api/admin')

    return app
