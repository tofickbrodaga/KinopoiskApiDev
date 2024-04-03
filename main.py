from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import create_engine
from model import Base, Movie, Actor
from sqlalchemy.orm import sessionmaker
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)

DATABASE_URL = "postgresql://test:test@localhost:37891/test"  # Подставьте свои данные
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


Base.metadata.create_all(engine)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        movies = search_movie(query, 'movie')
        return render_template('index.html', movies=movies, query=query)
    return render_template('index.html')

def get_movie_details(movie_id):
    url = f"https://api.kinopoisk.dev/v1.4/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": getenv('API_KEY')
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

@app.route('/add_movie/<movie_id>', methods=['POST'])
def add_movie(movie_id):
    movie = get_movie_details(movie_id)
    if movie:
        session = Session()
        movie_obj = Movie(
            name=movie['name'],
            year=movie['year'],
            rating_kp=movie['rating']['kp']
        )
        session.add(movie_obj)
        session.commit()
        session.close()
        return redirect(url_for('index'))
    else:
        return "Failed to fetch movie details"

def search_movie(query, search_type):
    if search_type == 'actor':
        url = f"https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=10&query={query}"
    else:
        url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query={query}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": getenv('API_KEY') # Ваш API ключ
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

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
    else:
        movies = session.query(Movie).all()
        session.close()
        return render_template('favorites.html', movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
