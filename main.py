from os import getenv

import requests
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import HEADERS, OK
from model import Actor, Base, Movie

load_dotenv()

app = Flask(__name__)

engine = create_engine(getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        search_type = request.form['search_type']
        if search_type == 'movies':
            srchd = search_movie(query)
        elif search_type == 'actors':
            srchd = search_actor(query)
        return render_template('index.html', results=srchd, query=query, search_type=search_type)
    return render_template('index.html', results=None)


def search_actor(query):
    url = f'https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=10&query={query}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == OK:
        return response.json()


def search_movie(query):
    url = f'https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query={query}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == OK:
        return response.json()


def get_actor_details(actor_id):
    url = f'https://api.kinopoisk.dev/v1.4/person/{actor_id}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == OK:
        return response.json()


def get_movie_details(movie_id):
    url = f'https://api.kinopoisk.dev/v1.4/movie/{movie_id}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == OK:
        return response.json()


@app.route('/add_actor/<actor_id>', methods=['POST'])
def add_actor(actor_id):
    actor = get_actor_details(actor_id)
    if actor and 'name' in actor:
        session = Session()
        actor_obj = Actor(
            name=actor['name'],
            enName=actor.get('enName', ''),
        )
        session.add(actor_obj)
        session.commit()
        session.close()
    return redirect(url_for('index'))


@app.route('/add_movie/<movie_id>', methods=['POST'])
def add_movie(movie_id):
    movie = get_movie_details(movie_id)
    if movie and 'name' in movie:
        session = Session()
        movie_obj = Movie(
            name=movie['name'],
            year=movie.get('year', 0),
            rating_kp=movie.get('rating', {}).get('kp', 0),
        )
        session.add(movie_obj)
        session.commit()
        session.close()
    return redirect(url_for('index'))


@app.route('/favourites', methods=['GET', 'POST'])
def favorites():
    session = Session()
    if request.method == 'POST':
        if 'movie_id' in request.form:
            movie_id = request.form['movie_id']
            movie = session.query(Movie).filter_by(id=movie_id).first()
            session.delete(movie)
        elif 'actor_id' in request.form:
            actor_id = request.form['actor_id']
            actor = session.query(Actor).filter_by(id=actor_id).first()
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
