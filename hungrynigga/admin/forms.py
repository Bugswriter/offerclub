from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField, IntegerField, SelectField, DateField
from wtforms.widgets import TextArea, html5
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_wtf.file import FileField, FileAllowed
from hungrynigga.models import Item


class ItemForm(FlaskForm):
	category_list = [
		('men','Mens Wear'),
		('women','Womens Wear'),
		('foods','Foods'),
		('banquet','Banquet lawn'),
		('hotels','Hotels'),
		('electronics','Electronics'),
		('parlour','Hair Saloon & Parlour'),
		('jwelery', 'Jwelery'),
		('stationary','Stationary'),
		('others','Others')
	]
	title = StringField('Offer Title', validators=[DataRequired()])
	discription = StringField('Add Offer Discription', widget=TextArea(), validators=[DataRequired()])
	image = FileField('Item Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	discount = IntegerField('Add Discount', widget=html5.NumberInput() ,validators=[DataRequired()])
	mrp = IntegerField('Original Price', widget=html5.NumberInput(), validators=[DataRequired()])
	exp = DateField('Offer Expiry Date (Format: MM/DD/YY)', format='%m/%d/%Y')
	category = SelectField('Category',  validators=[DataRequired()], choices=category_list)
	submit=SubmitField('Add Offer +')
