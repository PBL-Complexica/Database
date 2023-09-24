from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class app_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class email_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class user_email(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class phone_number(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class user_phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class device(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class user_device(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class category(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class user_category(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class subscription_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class user_subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
