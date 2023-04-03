from . import db
from flask_login import UserMixin
from flask_admin import Admin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    is_admin = db.Column(db.Boolean, default=False, index=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    cart = db.relationship('Cart', backref='user', uselist=False)

    def __repr__(self):
        return '{} {} {}'.format(self.email, self.password, self.username)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Float)
    out_of_stock = db.Column(db.Boolean, default=False, nullable=False)
    category = db.Column(db.String(50))
    orders = db.relationship('Order', backref='item')
    cart = db.relationship('Cart', backref='item', uselist=False)

    def __repr__(self):
        return "<Item>: {} ... {}".format(self.name, self.price)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "user: {} item: {}".format(self.user.username, self.item.name)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Integer)
    address = db.Column(db.String(100))
    contact_number = db.Column(db.Integer)
    delivered = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def order_price(self):
        return self.amount * self.item.price

    def __repr__(self):
        return "<order>: {}".format(self.item_id)

