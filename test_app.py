import pytest
from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    # Create tables before tests run
    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    # Optionally drop tables after tests
    with app.app_context():
        db.drop_all()


def test_home_status_code(client):
    response = client.get('/')
    assert response.status_code == 200
