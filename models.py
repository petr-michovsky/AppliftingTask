# ----------------------------------------------------- #
# --------- This file contains database models -------- #
# ----------------------------------------------------- #
from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    # One-to-many relationship for offers
    offers = db.relationship('Offer', back_populates='product', cascade='all, delete-orphan', lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "offers": [offer.to_dict() for offer in self.offers]
        }

    @classmethod
    def get_all_ids(cls):
        return [product.id for product in cls.query.all()]


class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    price = db.Column(db.Integer, nullable=False)
    items_in_stock = db.Column(db.Integer, nullable=False)

    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', back_populates='offers')

    def to_dict(self):
        return {
            'id': str(self.id),
            'price': self.price,
            'items_in_stock': self.items_in_stock,
            'product_id': str(self.product_id)
        }
