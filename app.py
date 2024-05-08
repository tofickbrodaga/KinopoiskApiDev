"""A module, which contains the main Flask app."""
import requests
from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL, GET, HEADERS, OK, POST
from model import Actor, Base, Movie

app = Flask(__name__)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


@app.route('/', methods=[GET, POST])
def index():
    """
    Handle the index route.

    Retrieve the query and search type from the form data,
    search for movies or actors based on the search type,
    and render the search results on the 'index.html' page.

    Parameters:
        None

    Returns:
        The rendered template with the search results, query, and search type.
    """
    if request.method == POST:
        query = request.form['query']
        search_type = request.form['search_type']
        if search_type == 'movies':
            srchd = search_movie(query)
        elif search_type == 'actors':
            srchd = search_actor(query)
        return render_template('index.html', results=srchd, query=query, search_type=search_type)
    return render_template('index.html', results=None)


def search_actor(query):
    """
    Search for actors based on a given query.

    Parameters:
        query (str): The search query for actors.

    Returns:
        list contains:
            - 'id' (int): The ID of the actor.
            - 'name' (str): The name of the actor.
            - 'enName' (str): The English name of the actor.
            - 'age' (int): The age of the actor.
            - 'rating' (float): The rating of the actor.

    If the response status code is not OK (200), an empty list is returned.
    """
    url = f'https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=10&query={query}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == OK:
        return response.json()
    return []


def search_movie(query):
    """
    Search for movies based on a given query.

    Parameters:
        query (str): The search query for movies.

    Returns:
        dict or list: A dictionary containing movie search results,
                      otherwise an empty list.
    """
    url = f'https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query={query}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == OK:
        return response.json()
    return []


def get_actor_details(actor_id):
    """
    Retrieve the details of an actor from the Kinopoisk API based on the provided actor ID.

    Parameters:
        actor_id (int): The ID of the actor to retrieve details for.

    Returns:
        dict: A dictionary containing the actor's details, including their name, age, and rating.
              If the actor ID is not found or an error occurs, an empty dictionary is returned.
    """
    url = f'https://api.kinopoisk.dev/v1.4/person/{actor_id}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == OK:
        return response.json()
    return {}


def get_movie_details(movie_id):
    """
    Retrieve the details of a movie from the Kinopoisk API based on the provided movie ID.

    Parameters:
        movie_id (int): The ID of the movie to retrieve details for.

    Returns:
        dict: A dictionary containing the movie's information.
              If the movie ID is not found or an error occurs, an empty dictionary is returned.
    """
    url = f'https://api.kinopoisk.dev/v1.4/movie/{movie_id}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == OK:
        return response.json()
    return {}


@app.route('/add_actor/<actor_id>', methods=[POST])
def add_actor(actor_id):
    """
    Add an actor to the database based on the provided actor ID.

    Parameters:
        actor_id (str): The ID of the actor to add.

    Returns:
        flask.wrappers.Response: A redirect response to the 'index' route.
    """
    actor = get_actor_details(actor_id)
    name = actor.get('name') or actor.get('enName', '')
    if name:
        session = Session()
        actor_obj = Actor(
            name=name,
        )
        session.add(actor_obj)
        session.commit()
        session.close()
    return redirect(url_for('index'))


@app.route('/add_movie/<movie_id>', methods=[POST])
def add_movie(movie_id):
    """
    Add a movie to the database based on the provided movie ID.

    Parameters:
        movie_id (str): The ID of the movie to add.

    Returns:
        flask.wrappers.Response: A redirect response to the 'index' route.
    """
    movie = get_movie_details(movie_id)
    name = movie.get('name') or movie.get('enName', '') or movie.get('alternativeName', '')
    if name:
        session = Session()
        movie_obj = Movie(
            name=name,
            year=movie.get('year', 'None'),
            rating_kp=movie.get('rating', {}).get('kp', 'None'),
        )
        session.add(movie_obj)
        session.commit()
        session.close()
    return redirect(url_for('index'))


@app.route('/favourites', methods=['GET', 'POST'])
def favourites():
    """
    Access the '/favourites' page: GET & DELETE.

    Deletes a movie or actor from the database based on the provided ID.

    Parameters:
        None

    Returns:
        A redirect response to the 'favourites' route if the request method is POST,
        otherwise a rendered template of the 'favourites.html' page with all movies and actors.
    """
    session = Session()
    if request.method == 'POST':
        if 'movie_id' in request.form:
            movie_id = request.form.get('movie_id')
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                session.delete(movie)
        elif 'actor_id' in request.form:
            actor_id = request.form.get('actor_id')
            actor = session.query(Actor).filter_by(id=actor_id).first()
            if actor:
                session.delete(actor)
        session.commit()
        session.close()
        return redirect(url_for('favourites'))
    movies = session.query(Movie).all()
    actors = session.query(Actor).all()
    session.close()
    return render_template('favourites.html', movies=movies, actors=actors)


if __name__ == '__main__':
    app.run(debug=True)
