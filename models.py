from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    vendor_sweets = db.relationship('VendorSweet', backref='vendor', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Sweet(db.Model):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    vendor_sweets = db.relationship('VendorSweet', backref='sweet', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class VendorSweet(db.Model):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'), nullable=False)

    @validates('price')
    def validate_price(self, key, price):
        if not price:
            raise ValueError("Price is required")
        if price < 0:
            raise ValueError("Price must be non-negative")
        return price

    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'vendor_id': self.vendor_id,
            'sweet_id': self.sweet_id
        }