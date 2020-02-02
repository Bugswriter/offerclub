from flask import Blueprint, render_template, redirect, url_for, flash
from hungrynigga.admin.utils import adminCheck, save_picture
from hungrynigga.admin.forms import ItemForm
from hungrynigga.models import Orderinfo
from hungrynigga import db
from random import randint
from hungrynigga.models import Item

admin = Blueprint('admin', __name__)


@admin.route('/additem', methods =['GET', 'POST'])
def additem():
	adminCheck()
	form =ItemForm()
	if form.validate_on_submit():
		if form.veg.data=='Veg':
			vegi=True
		else:
			vegi= False
		if form.image.data:
			picture_file=save_picture(form.image.data)
			item=Item(title=form.title.data,image=picture_file,mrp=form.mrp.data, category=form.category.data ,offer=randint(10,65), veg=vegi, rating=randint(30,100))
			db.session.add(item)
			db.session.commit()
			flash("Your item has been added",category='success')

	return render_template('additem.html', form =form)


@admin.route('/ordersview', methods =['GET', 'POST'])
def ordersview():
	adminCheck()
	orders=Orderinfo.query.all()
	return render_template('ordersview.html', orders=orders)

@admin.route('/ordersview/<int:oid>/<int:update>', methods =['GET','POST'])
def ordersviewupdate(oid, update):
	adminCheck()
	order=Orderinfo.query.get_or_404(oid)
	if update:
		order.status=order.status+1
	else:
		order.status=0
	db.session.commit()
	return redirect(url_for('admin.ordersview'))

