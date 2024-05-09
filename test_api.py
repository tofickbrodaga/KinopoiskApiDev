"""Tests for the API routes."""
from unittest.mock import patch

import pytest

from app import app
from config import MOVED, OK


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


@patch('app.get_actor_details')
def test_add_actor(mock_get_actor_details, client):
    """Test add actor to the database.

    Args:
        client (flask.testing.FlaskClient): The test client for the API.
        mock_get_actor_details: replaceable patch for creating a request.

    Return:
        None.
    """
    mock_actor_details = {
        'name': 'John Doe',
        'enName': 'John Doe',
        'age': 35,
    }
    mock_get_actor_details.return_value = mock_actor_details

    response = client.post('/add_actor/123')

    assert response.status_code == MOVED
    assert response.headers['Location'] == '/'


@patch('app.get_movie_details')
def test_add_movie(mock_get_movie_details, client):
    """Test add actor to the database.

    Args:
        client (flask.testing.FlaskClient): The test client for the API.
        mock_get_movie_details: replaceable patch for creating a request.

    Return:
        None.
    """
    mock_movie_details = {
        'name': 'Lion',
        'year': 2017,
        'rating_kp': 7.28,
    }

    mock_get_movie_details.return_value = mock_movie_details

    response = client.post('/add_movie/12')

    assert response.status_code == MOVED
    assert response.headers['Location'] == '/'


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
