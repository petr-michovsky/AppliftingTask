# ----------------------------------------------------- #
# -------- This file contains pytest fixtures --------- #
# ----------------------------------------------------- #
import pytest
from app import create_app
from models import db, Product
from config import TestConfig


@pytest.fixture()
def app():
    app = create_app(config_class=TestConfig)
    app.config.update({"TESTING": True})

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture(scope="function")
def session(app):
    with app.app_context():
        db.create_all()
        yield db.session


@pytest.fixture()
def product_data():
    return {
        "name": "Test Product",
        "description": "A product for testing"
    }


@pytest.fixture()
def offer_data():
    return {
        "price": 100,
        "items_in_stock": 50,
    }


@pytest.fixture
def sample_product(session):
    product_data = {
        'name': 'Test Product',
        'description': 'A product for testing'
    }
    product = Product(**product_data)
    session.add(product)
    session.commit()
    return product