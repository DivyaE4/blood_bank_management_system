from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[DataRequired()])
    blood_type = SelectField('Blood Type', choices=[
        ('A+', 'A+'), ('A-', 'A-'), 
        ('B+', 'B+'), ('B-', 'B-'), 
        ('AB+', 'AB+'), ('AB-', 'AB-'), 
        ('O+', 'O+'), ('O-', 'O-')
    ], validators=[DataRequired()])
    contact_info = StringField('Contact Info', validators=[
        DataRequired(), Length(min=10, max=10), 
        Regexp(r'^\d{10}$', message="Contact info must be a 10-digit number.")
    ])
    submit = SubmitField('Register')


class RequestForm(FlaskForm):
    blood_type = SelectField('Blood Type', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), 
                                                    ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), 
                                                    ('AB+', 'AB+'), ('AB-', 'AB-')],
                             validators=[DataRequired()])  # Dropdown for blood type
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    id_proof = FileField('Upload ID Proof', validators=[DataRequired()])  # File upload for ID proof
    submit = SubmitField('Submit Request')
