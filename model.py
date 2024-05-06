"""Model for movies and actors."""
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for declarative models."""

    pass


class Movie(Base):
    """Represents a movie in the database."""

    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    rating_kp = Column(Float)


class Actor(Base):
    """Represents an actor in the database."""

    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    enName = Column(String)
    age = Column(Integer)
