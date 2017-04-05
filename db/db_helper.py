from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base

def connect_to_database(app):
    """Connects to the database and returns an sqlalchemy session object."""
    print "connecting"
    engine = create_engine(app.config['DATABASE_URL'])
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()

    return session

def create_db(database_url):
    """Create an empty database with the tables defined above."""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    print "Database file created..."    