from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm
from models import db, User

app = Flask(__name__)


db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Logic to authenticate user
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# Similar routes for register, dashboard, etc.

if __name__ == '__main__':
    app.run()
