from flask import render_template, url_for, redirect, request, Blueprint, flash, current_app
from hungrynigga.users.forms import (RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm, FinalRegisterForm)
from hungrynigga import db, bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from hungrynigga.models import User, Orderinfo
from hungrynigga.users.utils import send_reset_email, send_confirmation_link
from flask_login import current_user, login_user, logout_user, login_required


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('items.menu'))

	registerform = RegisterForm()
	if registerform.validate_on_submit():
		send_confirmation_link(registerform.email.data)
		flash(f"Conformation link is on your email", 'success')
		return redirect(url_for('users.login'))

	return render_template('register.html', title='Register', form=registerform)

@users.route('/register/<token>', methods=['GET', 'POST'])
def finalregister(token):
	if current_user.is_authenticated:
		return redirect(url_for('items.menu'))
	s=Serializer(current_app.config['SECRET_KEY'])
	finalregisterform=FinalRegisterForm()
	try:
		email=s.loads(token)['email']
	except:
		email=None
	if not email:
		pass
	if finalregisterform.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(finalregisterform.password.data).decode('utf-8')
		user = User(username=finalregisterform.username.data, email=email, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f"You are successully Registered", 'success')
		return redirect(url_for('users.login'))
	return render_template('finalregister.html', title='Account Verification', form=finalregisterform)


@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('items.menu'))
	loginform = LoginForm()

	if loginform.validate_on_submit():
		user = User.query.filter_by(email=loginform.email.data).first()
		if user and bcrypt.check_password_hash(user.password, loginform.password.data):
			login_user(user, remember=loginform.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('items.menu'))
		else:
			flash(f'Login Unsuccessful. Please check email or password', 'danger')

		redirect(url_for('items.menu'))
	return render_template('login.html', title='Login', form=loginform)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('items.menu'))


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form=RequestResetForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with  instructions to reset your password.', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user=User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('reset_request'))
	form=ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password=hashed_password
		db.session.commit()
		flash("your account has been Updated! you are now able to log in", 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/account', methods=['GET'])
@login_required
def account():
	user = User.query.get_or_404(current_user.id)
	return render_template('account.html', user=user)


@users.route('/myorders', methods=['GET'])
@login_required
def myorders():
	orders=Orderinfo.query.filter_by(user_id=current_user.id)
	Zeroorder=False
	try:
		orders[0].address
	except:
		Zeroorder=True
	return render_template('myorders.html', orders=orders, Zeroorder=Zeroorder)

