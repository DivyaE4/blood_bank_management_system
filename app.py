from flask import Flask, render_template, redirect, url_for, request, flash, session
import mysql.connector
from forms import LoginForm, RegisterForm,AdminLoginForm  # Assuming you have these forms created
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
    
    return render_template('donate_location.html', camps=camps, username=session.get('username'))  # Pass username to the template




from flask import session  # Import session

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


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check if the admin exists in the MySQL database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = 'SELECT * FROM admin_details WHERE username = %s AND password = %s'
        cursor.execute(query, (username, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if admin:
            session['admin_id'] = admin['id']  # Store admin ID in session
            session['admin_username'] = admin['username']  # Store admin username in session
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))  # Redirect to an admin dashboard or home page
        else:
            flash('Invalid admin username or password.', 'danger')
    
    return render_template('admin_login.html', form=form)







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
            cursor.close()
            conn.close()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/camp/<int:id>', methods=['GET', 'POST'])
def camp_details(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch camp details
    cursor.execute("SELECT * FROM donation_camps WHERE id = %s", (id,))
    camp = cursor.fetchone()

    if not camp:
        flash('Camp not found.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Check if the user is logged in
        if 'user_id' not in session:
            flash('Please log in to make a donation.', 'danger')
            return redirect(url_for('login'))

        user_id = session['user_id']
        
        # Fetch the user's blood type
        cursor.execute("SELECT blood_type FROM login_details WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        blood_type = user['blood_type']

        camp_name = camp['camp_name']
        location = camp['location']
        timings = camp['timings']

        # Insert the donation into the donations table
        cursor.execute(
            "INSERT INTO donations (user_id, camp_id, camp_name, location, timings, blood_type) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, id, camp_name, location, timings, blood_type)
        )
        conn.commit()
        flash('Donation successful!', 'success')
        return redirect(url_for('index'))

    cursor.close()
    conn.close()

    return render_template('camp_details.html', camp=camp)

@app.route('/view-requests')
def view_requests():
    # Ensure user is logged in
    if 'user_id' not in session:
        flash('Please log in to view your requests.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    # Connect to the database and fetch requests made by the logged-in user
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = '''SELECT request_id, recipient_id, blood_type, quantity, request_date, status 
           FROM requests 
           WHERE recipient_id = %s 
           ORDER BY request_date DESC'''
    cursor.execute(query, (user_id,))
    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('view_requests.html', requests=requests, username=session.get('username'))



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
    if 'user_id' not in session:
        flash('Please log in to view your donations.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch donations made by the logged-in user
    cursor.execute('''SELECT d.camp_name, d.location, d.timings, dc.address 
                      FROM donations d
                      JOIN donation_camps dc ON d.camp_id = dc.id
                      WHERE d.user_id = %s''', (user_id,))
    donations = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('view_donations.html', donations=donations, username=session.get('username'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    session.pop('username', None)  # Remove username from session
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


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
                return redirect(url_for('request_status'))  # Redirect after successful submission
            except Exception as e:
                conn.rollback()
                flash(f'Error submitting request: {e}')
                print(f'Error: {e}')  # Log the error for debugging
        else:
            flash('Invalid file type. Please upload a valid image or PDF.')
    
    return render_template('make_request.html', form=form, username=username)

# Function to update inventory based on the current state of the donations table
def update_inventory():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Aggregate blood types and quantities from donations
    cursor.execute("""
        SELECT blood_type, SUM(quantity) AS total_units
        FROM donations
        GROUP BY blood_type
    """)
    results = cursor.fetchall()

    # Update inventory based on aggregated results
    for (blood_type, total_units) in results:
        # Check if the blood type exists in the inventory
        cursor.execute("SELECT qty FROM inventory WHERE blood_type = %s", (blood_type,))
        if cursor.fetchone():
            # Update the quantity for existing blood type
            cursor.execute("UPDATE inventory SET qty = %s WHERE blood_type = %s", (total_units, blood_type))
        else:
            # Insert new blood type into inventory if it doesn't exist
            cursor.execute("INSERT INTO inventory (blood_type, qty) VALUES (%s, %s)", (blood_type, total_units))

    connection.commit()
    cursor.close()
    connection.close()

# Function to handle blood requests by reducing inventory quantity
def handle_request(blood_type, requested_qty):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Check current quantity in inventory
    cursor.execute("SELECT qty FROM inventory WHERE blood_type = %s", (blood_type,))
    result = cursor.fetchone()
    if result and result[0] >= requested_qty:
        # Fulfill the request
        new_qty = result[0] - requested_qty
        cursor.execute("UPDATE inventory SET qty = %s WHERE blood_type = %s", (new_qty, blood_type))
        connection.commit()
        response = "Request fulfilled"
    else:
        response = "Insufficient quantity"

    cursor.close()
    connection.close()
    return response


@app.route('/admin/view_inventory')
def view_inventory():
    # Update inventory in real-time before displaying it
    update_inventory()
    
    # Retrieve inventory data
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('inventory.html', inventory=inventory)

@app.route('/admin/request_blood', methods=['POST'])
def request_blood():
    blood_type = request.form.get('blood_type')
    requested_qty = int(request.form.get('quantity'))
    result = handle_request(blood_type, requested_qty)
    flash(result)
    return redirect(url_for('view_inventory'))

# Confirmation page
@app.route('/request_status')
def request_status():
    return render_template('request_status.html')



if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for development
