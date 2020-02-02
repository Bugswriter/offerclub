from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from hungrynigga.models import User


class RegisterForm(FlaskForm):
	
	email = StringField('Email', validators=[DataRequired() ,Email()])
	submit = SubmitField('Register')	

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("That Email already exist")

class FinalRegisterForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("That Username already exist")


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
	email=StringField('Email', 
						validators=[DataRequired(), Email()])
	submit=SubmitField('Request Passwrod Reset')
	
	def validate_email(self, email):
		user=User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('Their is no account with that email.')

class ResetPasswordForm(FlaskForm):
	password=PasswordField('Password', 
						validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password', 
						validators=[DataRequired(), EqualTo('password')])
	submit=SubmitField('Reset Passwrod')

'''





hashed_password = bcrypt.generate_password_hash(registerform.password.data).decode('utf-8')
		user = User(username=registerform.username.data, email=registerform.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()

'''