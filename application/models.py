# from base import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# dbBind = {'order': 'sqlite:///database/order.db',
#           'ingress': 'sqlite:///database/ingress.db'}

class UserDb(UserMixin, db.Model):
    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    postalCode = db.Column(db.String(50), nullable=False)
    unitNumber = db.Column(db.String(200), nullable=False)
    accountType = db.Column(db.Integer, nullable=False)
    
class OrderDb(db.Model):
    __bind_key__ = 'order'
    orderId = db.Column(db.String(50), primary_key=True)
    customerId = db.Column(db.String(50), nullable=False)
    storeId = db.Column(db.String(50), nullable=False)
    orderDetails = db.Column(db.String(1000), nullable=False) # do we need this since we just doing 1 item per store
    status = db.Column(db.String(50), nullable=False)
    robotID = db.Column(db.String(50))
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

class IngressDb(db.Model):
    __bind_key__ = 'ingress'
    postalCode = db.Column(db.String(50), primary_key=True)
    ingressPoint = db.Column(db.String(200), nullable=False)
    
# db.create_all()