# app/models/__init__.py
"""
This file makes the models directory a Python package.
We can also use it to expose our models more conveniently.
"""

# app/models/__init__.py
"""
Database models package.

This file makes the models directory a Python package.
We import all models here for convenient access.
"""

# Import models in the correct order to avoid circular imports
# Owner first, then Pet (since Pet references Owner)
from app.models.owner import Owner
from app.models.pet import Pet, PetType

__all__ = ["Owner", "Pet", "PetType"]