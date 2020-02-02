from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange


class CheckoutForm(FlaskForm):
	name = StringField('Your Name', validators=[DataRequired()])
	contact = StringField('Phone Number', validators=[DataRequired(message="Enter Contact number"), Length(min=10)])
	address = StringField('Address', validators=[DataRequired()])
	zip_code = IntegerField("Area Code", validators=[DataRequired(), NumberRange(message="Invalid Area Code",min=1, max=999999)])
	submit = SubmitField('Place my Order')

