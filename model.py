from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    rating_kp = Column(Float)

class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    enName = Column(String)
    age = Column(Integer)