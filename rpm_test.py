import pytest
from main import app
from model import Actor, Movie
from sqlalchemy.orm import Session

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_favorites(client):
    response = client.get('/favorites')
    assert response.status_code == 200

def test_invalid_route(client):
    response = client.get('/invalid_route')
    assert response.status_code == 404

