from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
from models import User, Contact, Tracker
from database import db
import os

def create_app():
  app = Flask(__name__)
  db.init_app(app)
  
  return app
  
# Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///your_local_db_path.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(Config)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ... [rest of your routes and functions] ...
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

    
#Create a Route and Template for the Dashboard 
from flask_login import login_required

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

#a. Create a Route to Fetch and Display All Contacts (app.py):
@app.route('/database')
@login_required
def database_tab():
    contacts = Contact.query.all()
    return render_template('database.html', contacts=contacts)

#a. Create Routes to Handle Editing and Deleting Contacts (app.py):
from flask import request, flash, redirect, url_for

@app.route('/edit_contact/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        # Update contact details based on form data
        contact.name = request.form.get('name')
        contact.email = request.form.get('email')
        contact.phone = request.form.get('phone')
        contact.linkedin = request.form.get('linkedin')
        contact.twitter = request.form.get('twitter')
        contact.website = request.form.get('website')
        contact.speciality = request.form.get('speciality')
        contact.years_of_experience = int(request.form.get('experience'))
        contact.location = request.form.get('location')
        
        db.session.commit()
        flash('Contact updated successfully', 'success')
        return redirect(url_for('database_tab'))
    return render_template('edit_contact.html', contact=contact)

#a. Create a Route to Fetch and Display All Tracker Entries (app.py):
@app.route('/tracker')
@login_required
def tracker_tab():
    trackers = Tracker.query.all()
    return render_template('tracker.html', trackers=trackers)

#a. Create Routes to Handle Editing and Deleting Tracker Entries (app.py):
@app.route('/edit_tracker/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tracker(id):
    tracker = Tracker.query.get_or_404(id)
    if request.method == 'POST':
        # Update tracker details based on form data
        tracker.handler = request.form.get('handler')
        tracker.trainer_name = request.form.get('trainer_name')
        tracker.initial_outreach_date = request.form.get('initial_outreach_date')
        tracker.initial_outreach_channel = request.form.get('initial_outreach_channel')
        tracker.initial_outreach_reply = request.form.get('initial_outreach_reply')
        tracker.followup_1_date = request.form.get('followup_1_date')
        tracker.followup_1_channel = request.form.get('followup_1_channel')
        tracker.followup_1_reply = request.form.get('followup_1_reply')
        tracker.followup_2_date = request.form.get('followup_2_date')
        tracker.followup_2_channel = request.form.get('followup_2_channel')
        tracker.followup_2_reply = request.form.get('followup_2_reply')
        tracker.followup_3_date = request.form.get('followup_3_date')
        tracker.followup_3_channel = request.form.get('followup_3_channel')
        tracker.followup_3_reply = request.form.get('followup_3_reply')
        tracker.meeting_scheduled = request.form.get('meeting_scheduled')
        tracker.meeting_date = request.form.get('meeting_date')
        tracker.meeting_type = request.form.get('meeting_type')
        tracker.already_present = request.form.get('already_present')
        
        db.session.commit()
        flash('Tracker entry updated successfully', 'success')
        return redirect(url_for('tracker_tab'))
    return render_template('edit_tracker.html', tracker=tracker)

@app.route('/delete_tracker/<int:id>')
@login_required
def delete_tracker(id):
    tracker = Tracker.query.get_or_404(id)
    db.session.delete(tracker)
    db.session.commit()
    flash('Tracker entry deleted successfully', 'success')
    return redirect(url_for('tracker_tab'))

#1. Create a Route to Display and Handle the Add Contact Form (app.py):
@app.route('/add_contact', methods=['GET', 'POST'])
@login_required
def add_contact():
    if request.method == 'POST':
        # Fetch form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        linkedin = request.form.get('linkedin')
        twitter = request.form.get('twitter')
        website = request.form.get('website')
        speciality = request.form.get('speciality')
        years_of_experience = int(request.form.get('experience'))
        location = request.form.get('location')

        # Create a new Contact instance
        contact = Contact(name=name, email=email, phone=phone, linkedin=linkedin, twitter=twitter, website=website, speciality=speciality, years_of_experience=years_of_experience, location=location)

        # Add to the database
        db.session.add(contact)
        db.session.commit()

        flash('Contact added successfully', 'success')
        return redirect(url_for('database_tab'))

    return render_template('add_contact.html')


if __name__ == "__main__":
    app.run(debug=False)
