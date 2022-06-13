from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

db = create_engine(environ.get('DATABASE_URI', 'sqlite:///db.sqlite'), echo=True, future=True)
Base = declarative_base()
