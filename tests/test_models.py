# ----------------------------------------------------- #
# ------- This file contains tests for db models ------ #
# ----------------------------------------------------- #
from uuid import UUID
from models import Product, Offer


def test_create_product(product_data, session):
    product = Product(**product_data)
    session.add(product)
    session.commit()

    # Fetch the product from the database
    db_product = Product.query.first()

    assert db_product is not None
    assert db_product.name == product_data["name"]
    assert db_product.description == product_data["description"]
    assert isinstance(db_product.id, UUID)


def test_create_offer(offer_data, session):
    product = Product(name="Test Product", description="Product for offer testing")
    session.add(product)
    session.commit()

    offer = Offer(price=offer_data["price"], items_in_stock=offer_data["items_in_stock"], product_id=product.id)
    session.add(offer)
    session.commit()

    # Fetch the offer from the database
    db_offer = Offer.query.first()

    assert db_offer is not None
    assert db_offer.price == offer_data["price"]
    assert db_offer.items_in_stock == offer_data["items_in_stock"]
    assert db_offer.product_id == product.id


def test_product_offer_relationship(offer_data, product_data, session):
    product = Product(**product_data)
    session.add(product)
    session.commit()

    offer = Offer(price=offer_data["price"], items_in_stock=offer_data["items_in_stock"], product_id=product.id)
    session.add(offer)
    session.commit()

    # Fetch product and check its related offers
    db_product = Product.query.first()
    assert len(db_product.offers) == 1
    assert db_product.offers[0].price == offer_data["price"]


def test_to_dict(product_data, session):
    product = Product(**product_data)
    session.add(product)
    session.commit()

    # Test to_dict method
    db_product = Product.query.first()
    product_dict = db_product.to_dict()

    assert product_dict["id"] is not None
    assert product_dict["name"] == product_data["name"]
    assert product_dict["description"] == product_data["description"]
    assert isinstance(product_dict["offers"], list)


def test_get_all_ids(product_data, session):
    product = Product(**product_data)
    session.add(product)
    session.commit()

    # Test get_all_ids class method
    product_ids = Product.get_all_ids()
    assert len(product_ids) == 1
    assert isinstance(product_ids[0], UUID)  # Check if ID is UUID