from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class app_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class email_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class user_email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    email_id = db.Column(db.Integer, db.ForeignKey('email_address.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    removed_at = db.Column(db.DateTime, nullable=True, default='2100-01-01 00:00:00')


class phone_number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class user_phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    phone_id = db.Column(db.Integer, db.ForeignKey('phone_number.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    removed_at = db.Column(db.DateTime, nullable=True, default='2100-01-01 00:00:00')


class device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50), nullable=False)
    device_sn = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class user_device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    removed_at = db.Column(db.DateTime, nullable=True, default='2100-01-01 00:00:00')


class category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class user_category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    removed_at = db.Column(db.DateTime, nullable=True, default='2100-01-01 00:00:00')


class subscription_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription_type_name = db.Column(db.String(50), nullable=False)
    months = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription_type_id = db.Column(db.Integer, db.ForeignKey('subscription_type.id'), nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class user_subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    removed_at = db.Column(db.DateTime, nullable=True, default='2100-01-01 00:00:00')
