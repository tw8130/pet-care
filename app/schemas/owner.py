# app/schemas/owner.py
"""
Owner API schemas (request/response models).

These define what data the API accepts when creating/updating owners,
and what data it returns when you fetch owners.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

# Forward reference for PetResponse
if TYPE_CHECKING:
    from app.schemas.pet import PetResponse

class OwnerBase(BaseModel):
    """
    Base owner fields shared across different schemas.

    We create a base class to avoid repeating the same fields.
    Other schemas inherit from this.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Owner's full name")
    email: EmailStr = Field(..., description="Owner's email address")
    phone: str = Field(..., max_length=20, description="Contact phone number")


class OwnerCreate(OwnerBase):
    """
    Schema for creating a new owner.

    When someone POSTs to /api/v1/owners, their request body
    must match this schema.

    Notice: no 'id' field! The database generates that automatically.
    """
    pass  # Inherits all fields from OwnerBase, no additional fields needed


class OwnerUpdate(BaseModel):
    """
    Schema for updating an existing owner.

    All fields are optional because you might only want to update
    one field (like changing the phone number but not the email).
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)


class OwnerResponse(OwnerBase):
    """
    Schema for returning owner data to the client.

    This is what gets sent back when someone GETs /api/v1/owners/1

    Includes the database-generated fields (id, timestamps) that
    weren't in OwnerCreate.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    # NEW PYDANTIC V2 WAY ✅
    model_config = ConfigDict(from_attributes=True) # from_attributes=True means to  convert it to a Pydantic schema (for your API response)
    #class Config:
        # This allows Pydantic to work with SQLModel objects
        #from_attributes = True


class OwnerWithPets(OwnerResponse):
    """
    Schema for returning an owner with all their pets.

    Sometimes you want to return an owner and include their pets
    in one response. This schema does that.
    """
    pets: List["PetResponse"] = []  # Forward reference, defined in schemas/pet.py

 # This allows the forward reference to work at runtime
from app.schemas.pet import PetResponse
OwnerWithPets.model_rebuild()