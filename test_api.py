"""Tests for the API routes."""
import pytest

from config import MOVED, OK
from main import app


@pytest.fixture
def client():
    """
    Fixture to provide a test client for the application.

    Yields:
        flask.testing.FlaskClient: A test client for the application.
    """
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """
    Test the index route of the API.

    Args:
        client (flask.testing.FlaskClient): The test client for the API.

    Return:
        None
    """
    response = client.get('/')
    assert response.status_code == OK


def test_add_actor_route(client):
    """
    Test the add actor route of the API.

    Args:
        client (flask.testing.FlaskClient): The test client for the API.

    Return:
        None

    Raises:
        AssertionError: If the response status code is not MOVED (302).
    """
    response = client.post('/add_actor/1')
    assert response.status_code == MOVED


def test_add_movie_route(client):
    """
    Test the add movie route of the API.

    Args:
        client (flask.testing.FlaskClient): The test client for the API.

    Return:
        None

    Raises:
        AssertionError: If the response status code is not MOVED (302).
    """
    response = client.post('/add_movie/1')
    assert response.status_code == MOVED


def test_favorites_route(client):
    """
    Test the favorites route of the API.

    Args:
        client (flask.testing.FlaskClient): The test client for the API.

    Return:
        None

    Raises:
        AssertionError: If the response status code is not OK (200).
    """
    response = client.get('/favourites')
    assert response.status_code == OK
