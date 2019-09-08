"""
Connect to the database.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base

# Connects to the database and returns an sqlalchemy session object


def connect_database():
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session
