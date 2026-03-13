# PetCare API

A production-ready FastAPI application for managing pet care records.

## Features

- Owner management (CRUD operations)
- Pet management with owner relationships
- Input validation with Pydantic
- SQLite database with SQLModel ORM
- Comprehensive test coverage
- Professional project structure

## Technology Stack

- **FastAPI** - Modern web framework for building APIs
- **SQLModel** - SQL database toolkit that combines SQLAlchemy and Pydantic
- **UV** - Fast Python package manager
- **Pytest** - Testing framework

## Project Structure
```
petcare_api/
├── app/
│   ├── main.py              # Application entry point
│   ├── database.py          # Database configuration
│   ├── models/              # Database models
│   ├── schemas/             # API request/response schemas
│   ├── routers/             # API endpoints
│   └── core/                # Core configurations
└── tests/                   # Test files
```

## Setup Instructions

### 1. Install UV
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Setup
```bash
git clone <your-repo-url>
cd petcare_api

# UV automatically creates a virtual environment and installs dependencies
uv pip install -r requirements.txt
```

### 3. Run the Application
```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. View API Documentation

Open your browser and visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests
```bash
uv run pytest tests/ -v
```

## API Endpoints

### Owners

- `POST /api/v1/owners/` - Create a new owner
- `GET /api/v1/owners/` - List all owners
- `GET /api/v1/owners/{id}` - Get owner by ID (includes pets)
- `PATCH /api/v1/owners/{id}` - Update owner
- `DELETE /api/v1/owners/{id}` - Delete owner

### Pets

- `POST /api/v1/pets/` - Create a new pet
- `GET /api/v1/pets/` - List all pets
- `GET /api/v1/pets/{id}` - Get pet by ID
- `PATCH /api/v1/pets/{id}` - Update pet
- `DELETE /api/v1/pets/{id}` - Delete pet

## Example Usage

### Create an Owner
```bash
curl -X POST "http://localhost:8000/api/v1/owners/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+254712345678"
  }'
```

### Create a Pet
```bash
curl -X POST "http://localhost:8000/api/v1/pets/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Buddy",
    "pet_type": "dog",
    "breed": "Golden Retriever",
    "age": 3,
    "is_vaccinated": true,
    "owner_id": 1
  }'
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License