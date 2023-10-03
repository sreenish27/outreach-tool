from flask_login import UserMixin
from datetime import datetime
from app import db 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    phone = db.Column(db.String(20), unique=True)
    linkedin = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    website = db.Column(db.String(255))
    specialty = db.Column(db.String(80))
    years_of_experience = db.Column(db.Integer)
    location = db.Column(db.String(80))
    
    def __repr__(self):
        return f'<Contact {self.name}>'

class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handler = db.Column(db.String(80), nullable=False)
    trainer_name = db.Column(db.String(80), nullable=False)
    initial_outreach_date = db.Column(db.DateTime, default=datetime.utcnow)
    initial_outreach_channel = db.Column(db.String(50))
    initial_outreach_reply = db.Column(db.Boolean, default=False)

    followup_1_date = db.Column(db.DateTime)
    followup_1_channel = db.Column(db.String(50)) 
    followup_1_reply = db.Column(db.Boolean, default=False)

    meeting_scheduled = db.Column(db.Boolean, default=False)
    meeting_date = db.Column(db.DateTime)
    meeting_type = db.Column(db.String(50))
    already_present = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Tracker for {self.trainer_name}>'