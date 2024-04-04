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
    session = Session()
    actor_obj = Actor(
        name=actor['name'],
        year=actor['enName'],
    )
    session.add(actor_obj)
    session.commit()
    session.close()
    return redirect(url_for('index'))


@app.route('/add_movie/<movie_id>', methods=['POST'])
def add_movie(movie_id):
    movie = get_movie_details(movie_id)
    session = Session()
    movie_obj = Movie(
        name=movie['name'],
        year=movie['year'],
        rating_kp=movie['rating']['kp'],
    )
    session.add(movie_obj)
    session.commit()
    session.close()
    return redirect(url_for('index'))


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    session = Session()
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        movie = session.query(Movie).filter_by(id=movie_id).first()
        session.delete(movie)
        session.commit()
        session.close()
        return redirect(url_for('favorites'))
    movies = session.query(Movie).all()
    session.close()
    return render_template('favorites.html', movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
