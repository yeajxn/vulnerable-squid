from . import db
from datetime import datetime    


class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(1), nullable=False, default='U')
    cart = db.relationship('Cart', lazy=True)

class Card(db.Model):
    cardID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    image = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(10), nullable=False)
    text = db.Column(db.String(180), nullable=True)
    attack = db.Column(db.Integer, nullable=True)
    hp = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
class Cart(db.Model):
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), primary_key=True)
    cardID = db.Column(db.Integer, db.ForeignKey('card.cardID'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    cardInfo = db.relationship('Card', lazy=True)

class Order(db.Model):
    orderID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    total = db.Column(db.Float, nullable=False)
    cards = db.relationship('CardOrders', lazy=True)

class CardOrders(db.Model):
    orderID = db.Column(db.Integer, db.ForeignKey('order.orderID'), primary_key=True)
    cardID = db.Column(db.Integer, db.ForeignKey('card.cardID'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    cardInfo = db.relationship('Card', lazy=True)