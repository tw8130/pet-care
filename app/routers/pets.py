# app/routers/pets.py
"""
Pet API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.pet import Pet
from app.models.owner import Owner
from app.schemas.pet import PetCreate, PetUpdate, PetResponse

router = APIRouter(prefix="/pets", tags=["pets"])


@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet(
        pet_data: PetCreate,
        session: Session = Depends(get_session)
):
    """
    Create a new pet.

    Validates that the owner exists before creating the pet.
    """
    # Verify owner exists
    owner = session.get(Owner, pet_data.owner_id)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with id {pet_data.owner_id} not found"
        )

    # Owner confirmed — now create the pet
    db_pet = Pet.model_validate(pet_data)  #convert input model to table model to become a db row
    session.add(db_pet)  #track new pet added
    session.commit()     #save changes to db
    session.refresh(db_pet) # load the generated ID

    return db_pet


@router.get("/", response_model=List[PetResponse])
def get_pets(
        skip: int = 0,
        limit: int = 100,
        pet_type: str = None,
        session: Session = Depends(get_session)
):
    """
    Get all pets with optional filtering by type.
    """
    statement = select(Pet)

    # Optional filter by pet type
    if pet_type:
        statement = statement.where(Pet.pet_type == pet_type)

    # paginate (split into pages) your results.
    statement = statement.offset(skip).limit(limit)
    # .offset(0).limit(100) = "Start from the beginning, give me the first 100"
    # .offset(100).limit(100) = "Skip the first 100, give me the next 100"
    pets = session.exec(statement).all()

    return pets


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(
        pet_id: int,
        session: Session = Depends(get_session)
):
    """Get a specific pet by ID."""
    pet = session.get(Pet, pet_id)

    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pet with id {pet_id} not found"
        )

    return pet


@router.patch("/{pet_id}", response_model=PetResponse)
def update_pet(
        pet_id: int,
        pet_data: PetUpdate,
        session: Session = Depends(get_session)
):
    """Update an existing pet."""
    pet = session.get(Pet, pet_id)

    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pet with id {pet_id} not found"
        )

    # Update fields
    update_data = pet_data.model_dump(exclude_unset=True)
    #                                   ↑ "exclude_unset=True" means:
    #                                     ignore fields the user didn't include

    # Loop through and update each field
    for key, value in update_data.items():
        setattr(pet, key, value)
        # setattr is like saying: pet.name = "Miles"
        # but dynamically, for whatever fields were sent

    from datetime import datetime,timezone
    pet.updated_at = datetime.now(timezone.utc)

    session.add(pet)
    session.commit()
    session.refresh(pet)

    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(
        pet_id: int,
        session: Session = Depends(get_session)
):
    """Delete a pet."""
    pet = session.get(Pet, pet_id)

    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pet with id {pet_id} not found"
        )

    session.delete(pet)
    session.commit()

    # No content returned for successful DELETE (HTTP 204)
    return None