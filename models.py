from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'login_details'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    blood_type = db.Column(db.String(10), nullable=False)  # Field for blood type
    contact_info = db.Column(db.String(10), unique=True, nullable=False)  # Field for contact info

    def __repr__(self):
        return f'<User {self.username}>'

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(3), nullable=False)
    contact_info = db.Column(db.String(15), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('login_details.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('requests', lazy=True))
