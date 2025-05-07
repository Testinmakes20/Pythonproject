import pytest
from app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory DB for testing
    with app.app_context():
        db.create_all()  # Create tables before tests run
    with app.test_client() as client:
        yield client
    # Optionally drop tables after tests
    with app.app_context():
        db.drop_all()
