# app/main.py
"""
PetCare API - Main application entry point.
main.py is the traffic controller — it doesn't do the actual work, it directs requests to the right place.

This file creates the FastAPI application and connects all the routers.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager  #helps manage startup/shutdown events

from app.core.config import get_settings  #your settings binder
from app.database import create_db_and_tables  #the function that sets up your database
from app.routers import owners, pets   #your two routers

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler.

    Code before 'yield' runs when the application starts.
    Code after 'yield' runs when the application shuts down.

    This is where you do setup/teardown tasks like:
    - Creating database tables
    - Opening connections to external services
    - Closing connections when shutting down
    """
    # Startup: create database tables
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully!")

    yield  # Application runs here

    # Shutdown: cleanup tasks would go here
    print("Shutting down...")


# Create the FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan  # connect our startup/shutdown logic
)

# Include routers
app.include_router(owners.router, prefix=settings.api_prefix) #prefix=settings.api_prefix adds /api/v1 to the front of every route automatically.
app.include_router(pets.router, prefix=settings.api_prefix)


@app.get("/")
def read_root():
    """
    Root endpoint - health check.

    Returns basic API information.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.

    Used by monitoring tools to verify the API is running.
    """
    return {"status": "healthy"}