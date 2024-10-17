from flask_sqlalchemy import SQLAlchemy

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
