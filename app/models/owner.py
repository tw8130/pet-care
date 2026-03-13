# app/models/owner.py
"""
Owner database model.

This file defines what an Owner looks like in the database.
SQLModel will use this to create the actual database table.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime,timezone
#from app.models.pet import Pet

# Only import Pet for type checking, not at runtime
if TYPE_CHECKING:
    from app.models.pet import Pet

class Owner(SQLModel, table=True):
    """
    Represents a pet owner in the database.

    The 'table=True' parameter tells SQLModel: "this isn't just a Python class,
    this should become an actual table in the database."

    Each attribute becomes a column in the database table.
    """

    # Primary key - every row in the database needs a unique identifier
    # Optional[int] means it can be None initially (database will auto-generate it)
    id: Optional[int] = Field(default=None, primary_key=True)

    # Required fields (no default value means they must be provided)
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(unique=True, index=True)  # unique=True prevents duplicate emails
    phone: str = Field(max_length=20)

    # Timestamp fields - good practice to track when records are created/updated
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship: one owner can have many pets
    # This creates a link between Owner and Pet tables
    # back_populates="owner" means Pet table will have an "owner" field pointing back
    pets: List["Pet"] = Relationship(back_populates="owner")