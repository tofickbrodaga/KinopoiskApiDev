from flask import Flask, request, render_template, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import requests
from model import Actor, Movie
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'secret_key'

DATABASE_URL = os.getenv("DATABASE_URL")  # Используем переменную окружения для URL базы данных
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Favorite(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)

Base.metadata.create_all(engine)

def search_entity(query, entity_type):
    if entity_type == 'actor':
        url = f"https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=10&query={query}"
    else:
        url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query={query}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": os.getenv('API_KEY')
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    entity_type = request.form['entity_type']
    results = search_entity(query, entity_type)
    return render_template('search_results.html', movies=results.get('docs', []), query=query, entity_type=entity_type)

@app.route('/add_movie', methods=['POST'])
def add_movie():
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        # Добавление фильма в избранное
        favorite_movie = Favorite(name=movie_id, entity_type='movie')
        session = Session()
        session.add(favorite_movie)
        session.commit()
        session.close()
        flash('Added to favorites successfully!', 'success')
        return redirect(url_for('index'))
    else:
        return "Method Not Allowed", 405

@app.route('/add_actor', methods=['POST'])
def add_actor():
    if request.method == 'POST':
        actor_id = request.form['actor_id']
        # Добавление актера в избранное
        favorite_actor = Favorite(name=actor_id, entity_type='actor')
        session = Session()
        session.add(favorite_actor)
        session.commit()
        session.close()
        flash('Added to favorites successfully!', 'success')
        return redirect(url_for('index'))
    else:
        return "Method Not Allowed", 405

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    session = Session()
    if request.method == 'POST':
        entity_id = request.form['entity_id']
        entity_type = request.form['entity_type']
        if entity_type == 'movie':
            entity = session.query(Movie).filter_by(id=entity_id).first()
        else:
            entity = session.query(Actor).filter_by(id=entity_id).first()

        if entity:
            session.delete(entity)
            session.commit()
            flash('Deleted from favorites successfully!', 'success')
        else:
            flash('Failed to delete from favorites!', 'error')

        session.close()
        return redirect(url_for('favorites'))

    else:
        movies = session.query(Movie).all()
        actors = session.query(Actor).all()
        session.close()
        return render_template('favorites.html', movies=movies, actors=actors)


if __name__ == '__main__':
    app.run(debug=True)
