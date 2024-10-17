from flask import Flask, render_template, redirect, url_for, request, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from forms import LoginForm, RegisterForm, RequestForm  # Assuming you have these forms created
from config import SECRET_KEY, PASSWORD  # Replace with your secret key

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
    form = LoginForm()  # Ensure you have a LoginForm defined in your forms.py
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check if the user exists in the MySQL database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = 'SELECT * FROM login_details WHERE username = %s AND password = %s'  # Note: No password hashing here for simplicity
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['user_id'] = user['id']  # Store user ID in session
            session['username'] = user['username']  # Store username in session
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
            # Hash the password before storing
            hashed_password = generate_password_hash(password)
            # Insert new user if username is unique
            query = '''INSERT INTO login_details (username, password, age, blood_type, contact_info)
                       VALUES (%s, %s, %s, %s, %s)'''
            cursor.execute(query, (username, hashed_password, age, blood_type, contact_info))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# Dashboard route
@app.route('/dashboard')
def dashboard():
    # Ensure user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
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

# Route for the Request Management page
@app.route('/request', methods=['GET'])
def request1():
    return render_template('request.html')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/make-request', methods=['GET', 'POST'])
def make_request():
    form = RequestForm()

    # Ensure user is logged in, otherwise redirect
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Assuming you have a login route
    
    # Get the logged-in user's ID and username from the session
    recipient_id = session.get('user_id')
    username = session.get('username')

    if form.validate_on_submit():
        blood_type = form.blood_type.data
        quantity = form.quantity.data

        # Check if a file was uploaded
        if 'id_proof' not in request.files:
            flash('No file part')
            return redirect(request.url)

        id_proof = request.files['id_proof']  # This should work without issue

        # Validate file
        if id_proof and allowed_file(id_proof.filename):
            filename = secure_filename(id_proof.filename)
            file_data = id_proof.read()  # Read file as binary data (for BLOB)
            
            try:
                # Insert the request into the database
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO requests (recipient_id, blood_type, quantity, id_proof, status)
                                  VALUES (%s, %s, %s, %s, 'pending')''', 
                               (recipient_id, blood_type, quantity, file_data))
                conn.commit()
                cursor.close()
                conn.close()
                
                flash('Request submitted successfully!')
                return redirect(url_for('request_confirmation'))  # Redirect after successful submission
            except Exception as e:
                conn.rollback()
                flash(f'Error submitting request: {e}')
                print(f'Error: {e}')  # Log the error for debugging
        else:
            flash('Invalid file type. Please upload a valid image or PDF.')
    
    return render_template('make_request.html', form=form, username=username)

# Confirmation page
@app.route('/request-confirmation')
def request_confirmation():
    return "Your request has been submitted successfully!"

# Route for logging out
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for development
