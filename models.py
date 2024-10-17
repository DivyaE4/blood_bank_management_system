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

class DonationCamp(db.Model):
    __tablename__ = 'donation_camps'
    
    id = db.Column(db.Integer, primary_key=True)
    camp_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    timings = db.Column(db.String(255))
    address = db.Column(db.Text)
    
    def __init__(self, camp_name, location, timings, address):
        self.camp_name = camp_name
        self.location = location
        self.timings = timings
        self.address = address

class Request(db.Model):
    __tablename__ = 'requests'

    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('login_details.id'), nullable=False)
    blood_type = db.Column(db.String(3), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    request_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)

    def __repr__(self):
        return f'<Request {self.request_id}>'