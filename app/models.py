from app import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    pass_hash = db.Column(db.String(60), nullable=False)
    submissions = db.relationship('Submission', backref='user', lazy=True)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(22), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    info = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
