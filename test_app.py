import json
import pytest
from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()


def test_create_todo(client):
    data = {"title": "Test Task", "description": "Test description"}
    response = client.post(
        '/todos',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["title"] == "Test Task"


def test_get_todos(client):
    client.post('/todos', json={"title": "Task 1", "description": "Sample"})
    response = client.get('/todos')
    assert response.status_code == 200
    assert len(response.json) == 1


def test_update_todo(client):
    post_resp = client.post(
        '/todos',
        json={"title": "Initial", "description": "Before"}
    )
    todo_id = post_resp.json["id"]
    response = client.put(
        f'/todos/{todo_id}',
        json={"title": "Updated", "complete": True}
    )
    assert response.status_code == 200
    assert response.json["title"] == "Updated"
    assert response.json["complete"] is True


def test_delete_todo(client):
    post_resp = client.post(
        '/todos',
        json={"title": "To Delete", "description": "Temp"}
    )
    todo_id = post_resp.json["id"]
    response = client.delete(f'/todos/{todo_id}')
    assert response.status_code == 204
    response = client.get('/todos')
    assert len(response.json) == 0


def test_create_todo_invalid_payload(client):
    response = client.post(
        '/todos',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.json["error"] == "Title is required"
