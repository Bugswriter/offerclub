from hungrynigga.models import Orderitem
from flask_login import current_user

def getCartTotal():
	cart = Orderitem.query.filter_by(user_id=current_user.id, cart=True)
	mrptotal = 0
	realtotal = 0
	for item in cart:
		mrptotal += item.item.mrp*item.quantity
		realtotal += item.item.getOffer()*item.quantity

	return mrptotal, realtotal


