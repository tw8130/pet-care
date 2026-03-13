# app/models/pet.py
"""
Pet database model.

This defines the structure of pet records in the database.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, date, timezone
from enum import Enum
#from app.models.owner import Owner

# Only import Owner for type checking
if TYPE_CHECKING:
    from app.models.owner import Owner

class PetType(str, Enum):
    """
    Enumeration of pet types.

    Using an Enum ensures only valid pet types can be stored.
    This prevents typos like "Doog" instead of "Dog".
    """
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    RABBIT = "rabbit"
    OTHER = "other"


class Pet(SQLModel, table=True):
    """
    Represents a pet in the database.

    Each pet belongs to one owner (foreign key relationship).
    """

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Pet information
    name: str = Field(min_length=1, max_length=100)
    pet_type: PetType  # This uses our Enum above
    breed: Optional[str] = Field(default=None, max_length=100)
    age: Optional[int] = Field(default=None, ge=0, le=50)  # ge=0 means greater than or equal to 0
    date_of_birth: Optional[date] = None

    # Medical information
    weight_kg: Optional[float] = Field(default=None, gt=0)  # gt=0 means greater than 0
    is_vaccinated: bool = Field(default=False)
    medical_notes: Optional[str] = None

    # Foreign key - links this pet to an owner
    # This creates the relationship on the database level
    owner_id: int = Field(foreign_key="owner.id")

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship: each pet belongs to one owner
    owner: Optional["Owner"] = Relationship(back_populates="pets")