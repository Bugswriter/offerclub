from flask import Blueprint, request, render_template, jsonify, abort, redirect, flash
from flask_login import current_user, login_required
from hungrynigga import db
from hungrynigga.models import Item, Orderitem
from hungrynigga.items.utils import getCartTotal


items = Blueprint('items', __name__)


@items.route('/', methods=['GET'])
@items.route('/home', methods=['GET'])
def menu():
	items = Item.query.all()
	total = 0
	if current_user.is_authenticated:
		try:
			cart = Orderitem.query.filter_by(user_id=current_user.id, cart=True)

		except Exception as e:
				print(e)

		data = []
		for item in items:
			x = {}
			x['id'] = item.id
			x['title'] = item.title
			x['image'] = item.image
			x['mrp'] = item.mrp
			x['offer'] = item.offer
			x['rating'] = item.rating
			x['realprice'] = item.getOffer()
			x['category'] = item.category
			x['exp'] = item.date
			x['discription'] = item.discription
			x['cart'] = False
			x['rating_color'] = item.getRatingColor()
			for c in cart:
				if item == c.item:
					x['quantity'] = c.quantity
					x['cart'] = True

			data.append(x)

			total = getCartTotal()


		return render_template('menu.html', items=data, total=total)

	return render_template('menu.html', items=items)



@items.route('/addtocart', methods=['GET'])
def addcart():
	if not current_user.is_authenticated:
		abort(403)

	item_id = request.args.get('item_id')
	quantity = request.args.get('quantity')
	if item_id is None or quantity is None:
		abort(500)

	itemObj = Item.query.filter_by(id=item_id).first()

	cartitem = Orderitem.query.filter_by(item_id=item_id, user_id=current_user.id, cart=True).first();
	if cartitem is None:
		added = True
		cartitem = Orderitem(item_id=item_id, quantity=quantity, user_id=current_user.id)
		db.session.add(cartitem)
		db.session.commit()
	else:
		added = False
		db.session.delete(cartitem)
		db.session.commit()

	x = getCartTotal()
	item = {}
	item['id'] = itemObj.id
	item['title'] = itemObj.title
	item['quantity'] = quantity
	item['realprice'] = itemObj.getOffer()
	item['added'] = added
	item['mrptotal'] = x[0]
	item['realtotal'] = x[1]

	return jsonify(item)



