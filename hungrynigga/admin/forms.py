from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_wtf.file import FileField, FileAllowed
from hungrynigga.models import Item


class ItemForm(FlaskForm):
	title = StringField('Food Title', validators=[DataRequired()])
	image = FileField('Food Picture', validators=[FileAllowed(['jpg', 'png'])])
	mrp = IntegerField('Original Price')
	category = StringField('Category', validators=[DataRequired()])
	veg=SelectField('Food Type', validators=[DataRequired(), Optional()], choices=[('Veg','Veg'), ('Non-Veg', 'Non-Veg')])
	submit=SubmitField('Add Item +')
