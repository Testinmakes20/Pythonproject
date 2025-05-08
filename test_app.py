import json
import pytest
from app import app, db


@pytest.fixture


def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
    with app.app_context():
        db.create_all()  # Create all tables before each test
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()  # Clean up the database after tests

def test_create_todo(client):
    data = {"title": "Test Task", "description": "Test description"}
    response = client.post('/todos', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["title"] == "Test Task"

def test_get_todos(client):
    # Prepopulate a todo
    client.post('/todos', json={"title": "Task 1", "description": "Sample"})
    response = client.get('/todos')
    assert response.status_code == 200
    assert len(response.json) == 1  # We should have one todo

def test_update_todo(client):
    # First, create a todo
    post_resp = client.post('/todos', json={"title": "Initial", "description": "Before"})
    todo_id = post_resp.json["id"]
    response = client.put(f'/todos/{todo_id}', json={"title": "Updated", "complete": True})
    assert response.status_code == 200
    assert response.json["title"] == "Updated"
    assert response.json["complete"] is True

def test_delete_todo(client):
    # First, create a todo
    post_resp = client.post('/todos', json={"title": "To Delete", "description": "Temp"})
    todo_id = post_resp.json["id"]
    response = client.delete(f'/todos/{todo_id}')
    assert response.status_code == 204
    # Verify the todo is deleted
    response = client.get('/todos')
    assert len(response.json) == 0

def test_create_todo_invalid_payload(client):
    response = client.post('/todos', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400  # Assuming the route requires title
    assert response.json["error"] == "Title is required"
