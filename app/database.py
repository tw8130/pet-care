# app/database.py
"""
Database engine and session management.

This file is responsible for:
1. Creating the connection to the database
2. Creating all tables when the app starts
3. Providing database sessions to your API endpoints
"""

from sqlmodel import SQLModel, create_engine, Session
from app.core.config import get_settings

# Get our configuration
settings = get_settings()

# Create the database engine
# The engine is like a factory that creates connections to your database
# echo=True makes SQLModel print all SQL queries (useful for learning/debugging)
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Only show SQL queries in debug mode
    connect_args={"check_same_thread": False}  # Needed for SQLite
)


def create_db_and_tables():
    """
    Create all database tables.

    This function looks at all your SQLModel classes (Pet, Owner, etc.)
    and creates the corresponding tables in the database.

    Call this once when your application starts.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Provide a database session for each request.

    This is a "dependency" that FastAPI will call automatically.
    It creates a fresh database session, lets your code use it,
    then closes it when done.

    Think of a session like checking out a book from a library:
    1. You get a session (check out the book)
    2. You use it to read/write data (read the book)
    3. The session closes (return the book)

    The 'yield' keyword makes this a generator. FastAPI knows to:
    - Run everything before 'yield' at the start of a request
    - Run everything after 'yield' at the end of a request

    Yields:
        Session: A database session for this request
    """
    with Session(engine) as session:
        yield session