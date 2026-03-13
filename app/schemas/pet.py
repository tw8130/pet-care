# app/schemas/pet.py
"""
Pet API schemas (request/response models).
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional
from app.models.pet import PetType


class PetBase(BaseModel):
    """Base pet fields."""
    name: str = Field(..., min_length=1, max_length=100)
    pet_type: PetType
    breed: Optional[str] = Field(None, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=50)
    date_of_birth: Optional[date] = None
    weight_kg: Optional[float] = Field(None, gt=0)
    is_vaccinated: bool = False
    medical_notes: Optional[str] = None


class PetCreate(PetBase):
    """
    Schema for creating a new pet.

    Requires owner_id to link the pet to an owner.
    """
    owner_id: int = Field(..., description="ID of the pet's owner")


class PetUpdate(BaseModel):
    """
    Schema for updating a pet.

    All fields optional - update only what you need.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    pet_type: Optional[PetType] = None
    breed: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=70)
    date_of_birth: Optional[date] = None
    weight_kg: Optional[float] = Field(None, gt=0)
    is_vaccinated: Optional[bool] = None
    medical_notes: Optional[str] = None


class PetResponse(PetBase):
    """
    Schema for returning pet data.
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    # NEW PYDANTIC V2 WAY ✅
    model_config = ConfigDict(from_attributes=True)
    #class Config:
        #from_attributes = True