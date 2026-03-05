# tests/test_main.py
"""
Tests for the PetCare API.

These tests verify that your API endpoints work correctly.
"""

from fastapi.testclient import TestClient  #a fake browser that sends requests to your API
from sqlmodel import Session, create_engine, SQLModel  # creates a database connection
from sqlmodel.pool import StaticPool #keeps one shared connection for testing

from app.main import app  #your actual FastAPI application
from app.database import get_session  #the database session we're going to replace during tests

# Create an in-memory SQLite database for testing
# This database is created fresh for each test and deleted after
test_engine = create_engine(
    "sqlite://",  # In-memory database
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Reuse the same connection
)


def get_test_session():
    """Override the real database session for test database."""
    with Session(test_engine) as session:
        yield session


# Override the real dependency to use test database
app.dependency_overrides[get_session] = get_test_session

# Create test client
client = TestClient(app) #client is your fake browser. Instead of opening Postman or a real browser, you use client.get(...), client.post(...) etc. in your test code.


def setup_function():
    """
    Run before each test.

    Creates fresh database tables for each test so tests don't interfere
    with each other.
    """
    SQLModel.metadata.create_all(test_engine)


def teardown_function():
    """
    Run after each test.

    Drops all tables to ensure clean state.
    """
    SQLModel.metadata.drop_all(test_engine)


def test_read_root():
    """Test the root endpoint returns correct information."""
    response = client.get("/")
    # assert means "I'm asserting (claiming) this must be true. If it's not, the test fails."
    assert response.status_code == 200  # Did we get a good response?
    data = response.json()
    assert data["name"] == "PetCare API"   # Is the name correct?
    assert data["status"] == "running"    # Is it running?


def test_create_owner():
    """Test creating a new owner."""
    owner_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+254712345678"
    }

    response = client.post("/api/v1/owners/", json=owner_data)

    # Should return 201 Created
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == owner_data["name"]
    assert data["email"] == owner_data["email"]
    assert "id" in data  # Database should generate an ID


def test_create_duplicate_owner():
    """Test that creating an owner with duplicate email fails."""
    owner_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "+254712345679"
    }

    # Create first owner
    response1 = client.post("/api/v1/owners/", json=owner_data)
    assert response1.status_code == 201

    # Try to create duplicate
    response2 = client.post("/api/v1/owners/", json=owner_data)

    # Should return 409 Conflict
    assert response2.status_code == 409
    assert "already exists" in response2.json()["detail"]


def test_get_owner_not_found():
    """Test getting a non-existent owner returns 404."""
    response = client.get("/api/v1/owners/9999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_create_pet_with_owner():
    """Test creating a pet linked to an owner."""
    # First create an owner
    owner_data = {
        "name": "Pet Owner",
        "email": "petowner@example.com",
        "phone": "+254712345680"
    }
    owner_response = client.post("/api/v1/owners/", json=owner_data)
    owner_id = owner_response.json()["id"]  # Save the generated ID

    # Now create a pet
    pet_data = {
        "name": "Buddy",
        "pet_type": "dog",
        "breed": "Golden Retriever",
        "age": 3,
        "is_vaccinated": True,
        "owner_id": owner_id  #Link to the owner we just created
    }

    pet_response = client.post("/api/v1/pets/", json=pet_data)

    assert pet_response.status_code == 201
    pet = pet_response.json()
    assert pet["name"] == "Buddy"
    assert pet["owner_id"] == owner_id


def test_create_pet_with_invalid_owner():
    """Test that creating a pet with non-existent owner fails."""
    pet_data = {
        "name": "Orphan Pet",
        "pet_type": "cat",
        "owner_id": 9999  # Non-existent owner
    }

    response = client.post("/api/v1/pets/", json=pet_data)

    # Should return 404 because owner doesn't exist
    assert response.status_code == 404