from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm, RegisterForm  # Make sure to create a RegisterForm
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:18harini@localhost/donation_db'
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
            return redirect(url_for('dashboard'))  # Redirect to a dashboard or home page
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # Ensure you have a RegisterForm created
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        age = form.age.data
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Insert new user if username is unique
            new_user = User(username=username, password=password, age=age)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

# Example dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()
