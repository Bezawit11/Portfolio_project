from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Signup')

class AdminForm(FlaskForm):
    item_name = StringField('Item name', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    category = RadioField('Category', choices=[('Fruits','Fruits'),('Vegetables','Vegetables'), ('Dairy','Dairy'), ('Bread and baked goods','Bread and baked goods')
        , ('Meat and fish','Meat and fish'), ('Cans and jars','Cans and jars'), ('Pasta, rice and cereals','Pasta, rice and cereals'), 
        ('Sauces and condiments','Sauces and condiments'), ('Herbs and spices','Herbs and spices'), ('Frozen foods','Frozen foods'), ('Snacks','Snacks'), ('Drinks','Drinks'        ), ('Household and cleaning','Household and cleaning'), ('Personal care','Personal care'), ('Baby products','Baby products'), ('Other','Other')], 
        validators=[DataRequired()])
    submit = SubmitField('Add Item')
