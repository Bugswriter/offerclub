from flask import Blueprint, render_template, flash, abort, url_for, redirect
from flask_login import current_user, login_required
from hungrynigga.orders.forms import CheckoutForm
from hungrynigga importp db
from hungrynigga.models import Orderinfo, Orderitem

orders = Blueprint('orders', __name__)

@orders.route('/checkout', methods=['POST', 'GET'])
@login_required
def checkout():
	form = CheckoutForm()
	cart = Orderitem.query.filter_by(user_id=current_user.id, cart=True)
	print(list(cart))
	if list(cart) == []:
		flash(f"You need to add items in cart for checkout", 'info')
		return redirect(url_for('items.menu'))

	if form.validate_on_submit():
		order = Orderinfo(address=str(form.address.data), phone=form.contact.data, zip_code=int(form.zip_code.data), user_id=current_user.id)
		db.session.add(order)
		db.session.commit()
		for item in cart:
			item.cart = False
			item.order_id = order.id 
			db.session.commit()
			
		flash(f"Your order has been placed!!", 'success')
		return redirect(url_for('items.menu'))
		
	return render_template('checkout.html', form=form, cart=cart)


@orders.route('/order/<int:id>')
@login_required
def OrderDetail(id):
	try:
		order=Orderinfo.query.get_or_404(id)
		items=Orderitem.query.filter_by(order_id=order.id)
		if current_user.id==order.user_id:
			return render_template('orderdetail.html', order=order, items=items)
		else:
			pass
	except:
		return "ki"