import pytest
from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200


def test_search_movie(client):
    response = client.post('/', data={'query': 'Inception', 'search_type': 'movies'})
    assert response.status_code == 200


def test_search_actor(client):
    response = client.post('/', data={'query': 'Leonardo DiCaprio', 'search_type': 'actors'})
    assert response.status_code == 200


def test_add_actor_route(client):
    response = client.post('/add_actor/1')
    assert response.status_code == 302


def test_add_movie_route(client):
    response = client.post('/add_movie/1')
    assert response.status_code == 302


def test_favorites_route(client):
    response = client.get('/favourites')
    assert response.status_code == 200
