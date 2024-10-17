from flask import Flask, render_template, redirect, url_for, request, flash
import mysql.connector
from forms import LoginForm, RegisterForm  # Assuming you have these forms created
from config import SECRET_KEY  # Replace with your secret key
from config import PASSWORD

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Helper function to connect to the MySQL database
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',      # Your MySQL host
        user='root',           # Your MySQL username
        password=PASSWORD,     # Your MySQL password
        database='donation_db'  # Database name
    )
    return conn

# Home page route
@app.route('/')
def home():
    return render_template('home.html')

# Donation location route with filtering
@app.route('/donate-location', methods=['GET'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get the location filter from the URL parameters (if provided)
    location = request.args.get('location', None)
    
    if location:
        # Fetch donation camps based on location (case-insensitive)
        query = 'SELECT * FROM donation_camps WHERE LOWER(location) LIKE LOWER(%s)'
        cursor.execute(query, ('%' + location + '%',))
    else:
        # Fetch all donation camps if no location is specified
        query = 'SELECT * FROM donation_camps'
        cursor.execute(query)
    
    camps = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('donate_location.html', camps=camps)

# Route for viewing details of a specific donation camp
@app.route('/camp/<int:id>')
def camp_details(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch camp details by ID
    query = 'SELECT * FROM donation_camps WHERE id = %s'
    cursor.execute(query, (id,))
    camp = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if camp is None:
        return "No such camp found."
    
    return render_template('camp_details.html', camp=camp)

# Route for user login
@app.route('/donor_recipient', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check if the user exists in the MySQL database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = 'SELECT * FROM login_details WHERE username = %s AND password = %s'  # No password hashing here for simplicity
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to a dashboard or home page
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html', form=form)

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        age = form.age.data
        blood_type = form.blood_type.data
        contact_info = form.contact_info.data
        
        # Check if the username already exists
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM login_details WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Insert new user if username is unique
            query = '''INSERT INTO login_details (username, password, age, blood_type, contact_info)
                       VALUES (%s, %s, %s, %s, %s)'''
            cursor.execute(query, (username, password, age, blood_type, contact_info))
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        
        cursor.close()
        conn.close()
    
    return render_template('register.html', form=form)

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Donation-related routes
@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/make-donation')
def make_donation():
    return render_template('make_donation.html')

@app.route('/view-donations')
def view_donations():
    return render_template('view_donations.html')

if __name__ == '__main__':
    app.run()
