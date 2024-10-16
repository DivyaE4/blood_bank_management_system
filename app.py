from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm, RegisterForm  # Make sure to create a RegisterForm
from models import db, User
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database
db.init_app(app)

# Create tables before the first request using app context
with app.app_context():
    db.create_all()  # This will create the login_details table if it doesn't exist

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/donor_recipient', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check if the user exists
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # You might want to hash passwords for security
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to a information or home page
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        age = form.age.data
        blood_type = form.blood_type.data  # Get the blood type
        contact_info = form.contact_info.data  # Get the contact info
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Insert new user if username is unique
            new_user = User(username=username, password=password, age=age, blood_type=blood_type, contact_info=contact_info)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))  # Redirect to login page

    return render_template('register.html', form=form)


# Example dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route for the Request Management page
@app.route('/request', methods=['GET'])
def request():
    return render_template('request.html')

# # Route for making a request
# @app.route('/make_request', methods=['GET', 'POST'])
# def make_request():
#     if flask_request.method == 'POST':
#         # Here you would handle the logic to add the request to the database
#         blood_type = flask_request.form.get('blood_type')  # Get blood type from the form
#         contact_info = flask_request.form.get('contact_info')  # Get contact info from the form
#         user_id = 1  # Replace with the actual logged-in user ID
#         new_request = Request(blood_type=blood_type, contact_info=contact_info, user_id=user_id)
#         db.session.add(new_request)
#         db.session.commit()
#         flash('Your request has been submitted!', 'success')
#         return redirect(url_for('request_management'))

#     return render_template('make_request.html')

# # Route for viewing past requests
# @app.route('/view_requests', methods=['GET'])
# def view_requests():
#     # Query for past requests of the logged-in user
#     user_id = 1  # Replace with the actual logged-in user ID
#     past_requests = Request.query.filter_by(user_id=user_id).all()
#     return render_template('view_requests.html', requests=past_requests)

if __name__ == '__main__':
    app.run()
