# --------------------------------------------------------------------------------- #
# This file configures the application when using the create_app function in app.py #
# --------------------------------------------------------------------------------- #
import os


# Basic app configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', "default_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database.db")


# App configuration for testing purposes
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    DEBUG = False