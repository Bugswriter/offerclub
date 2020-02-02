from hungrynigga import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	orders = db.relationship('Orderinfo', backref='customer', lazy=True)

	def get_reset_token(self, expires_secs=1800):
		s=Serializer(current_app.config['SECRET_KEY'], expires_secs)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s=Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id=s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)	

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(300), nullable=False)
	discription = db.Column(db.Text(300), nullable=False)
	image = db.Column(db.String(20), nullable=False, default='default.jpg')
	mrp = db.Column(db.Integer, nullable=False)
	offer = db.Column(db.Integer, nullable=False, default=0)
	date = db.Column(db.String(30), nullable=False)
	rating = db.Column(db.Integer, nullable=True)
	category = db.Column(db.String(400), nullable=True)
	orders = db.relationship('Orderitem', backref='item', lazy=True)

	def getOffer(self):
		tagprice = self.mrp
		realprice = int(tagprice*((100-self.offer)/100))
		return realprice


	def getRatingColor(self):
		if self.rating <= 33:
			return "danger"
		elif self.rating > 33  and self.rating < 65:
			return "warning"
		else:
			return "success"


	def __repr__(self):
		return f"Item('{self.title}', '{self.mrp}', '{self.rating}', '{self.offer}')"



class Orderinfo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	order = db.relationship('Orderitem', backref='order', lazy=True)
	address = db.Column(db.String(300), nullable=False)
	phone = db.Column(db.Integer, nullable=False)
	zip_code = db.Column(db.Integer, nullable=False)
	time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	status = db.Column(db.Integer, nullable=False, default=1)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	

	def getStatus(self):
		if self.status == 0:
			return "Order Canceled"
		elif self.status == 1:
			return "Order has been placed"
		elif self.status == 2:
			return "Food is getting prepared"
		elif self.status == 3:
			return "Your order is out for delivery"
		elif self.status == 4:
			return "Your order has been successfully delivered"
		else:
			return "We have no track of your order"


	def getTotalAmount(self):
		totalAmount = 0
		order = self.order
		for x in order:
			temp = x.item.getOffer()
			totalAmount += int(temp[1])

		return totalAmount


	def __repr__(self):
		return f"Orderinfo('{self.address}', '{self.time}', '{self.getStatus()}')"


class Orderitem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	order_id = db.Column(db.Integer, db.ForeignKey('orderinfo.id'), nullable=True)
	cart = db.Column(db.Boolean, nullable=False, default=True)

	def __repr__(self):
		return f"Orderitem('{self.item_id}', '{self.quantity}', '{self.order_id}')"