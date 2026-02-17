# app/routers/owners.py
"""
Owner API endpoints.

This file contains all the routes (endpoints) for managing owners.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.owner import Owner
from app.schemas.owner import OwnerCreate, OwnerUpdate, OwnerResponse, OwnerWithPets
from datetime import datetime, date, timezone

# Create a router for owner-related endpoints
# The prefix="/owners" means all routes here start with /owners
# tags=["owners"] groups these endpoints in the API documentation
router = APIRouter(prefix="/owners", tags=["owners"])


@router.post("/", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
def create_owner(
        owner_data: OwnerCreate,
        session: Session = Depends(get_session)
):
    """
    Create a new pet owner.

    Args:
        owner_data: The owner information from the request body
        session: Database session (injected by FastAPI)

    Returns:
        The newly created owner

    Raises:
        HTTPException 409: If an owner with this email already exists
    """
    # Check if email already exists
    statement = select(Owner).where(Owner.email == owner_data.email)
    existing_owner = session.exec(statement).first()

    if existing_owner:
        # HTTP 409 Conflict: the request conflicts with existing data
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Owner with email {owner_data.email} already exists"
        )

    # Create new owner from the validated data
    db_owner = Owner.model_validate(owner_data) #convert input model to table model to become a db row

    # Add to database
    session.add(db_owner)
    session.commit()  # Save changes to database
    session.refresh(db_owner)  # Reload to get database-generated fields (like id)

    return db_owner


@router.get("/", response_model=List[OwnerResponse])
def get_owners(
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(get_session)
):
    """
    Get all owners with pagination.

    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        session: Database session

    Returns:
        List of owners
    """
    # paginate (split into pages) your results.
    statement = select(Owner).offset(skip).limit(limit)   #.offset(0).limit(100) = "Start from the beginning, give me the first 100"
    #.offset(100).limit(100) = "Skip the first 100, give me the next 100"
    owners = session.exec(statement).all()
    return owners


@router.get("/{owner_id}", response_model=OwnerWithPets)
def get_owner(
        owner_id: int,
        session: Session = Depends(get_session)
):
    """
    Get a specific owner by ID, including their pets.

    Args:
        owner_id: The owner's ID from the URL path
        session: Database session

    Returns:
        The owner with their pets

    Raises:
        HTTPException 404: If owner not found
    """
    owner = session.get(Owner, owner_id)   # Look for owner with this ID

    if not owner:
        # HTTP 404 Not Found: the requested resource doesn't exist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with id {owner_id} not found"
        )

    return owner # Returns owner + their pets (OwnerWithPets schema)


@router.patch("/{owner_id}", response_model=OwnerResponse)
def update_owner(
        owner_id: int,
        owner_data: OwnerUpdate,
        session: Session = Depends(get_session)
):
    """
    Update an existing owner.

    Args:
        owner_id: The owner's ID
        owner_data: Fields to update
        session: Database session

    Returns:
        The updated owner

    Raises:
        HTTPException 404: If owner not found
    """
    owner = session.get(Owner, owner_id)

    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with id {owner_id} not found"
        )

    # Update only the fields that were provided
    update_data = owner_data.model_dump(exclude_unset=True)
    #                                   ↑ "exclude_unset=True" means:
    #                                     ignore fields the user didn't include

    # Loop through and update each field
    for key, value in update_data.items():
        setattr(owner, key, value)
        # setattr is like saying: owner.phone = "+254799999999"
        # but dynamically, for whatever fields were sent

    # Update the timestamp
    from datetime import datetime
    owner.updated_at = datetime.now(timezone.utc)

    session.add(owner)
    session.commit()
    session.refresh(owner)

    return owner


@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_owner(
        owner_id: int,
        session: Session = Depends(get_session)
):
    """
    Delete an owner.

    Args:
        owner_id: The owner's ID
        session: Database session

    Raises:
        HTTPException 404: If owner not found
        HTTPException 400: If owner still has pets
    """
    owner = session.get(Owner, owner_id)

    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with id {owner_id} not found"
        )

    # Business rule: don't delete owners who still have pets
    if owner.pets:
        # HTTP 400 Bad Request: the request is invalid due to business rules
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete owner with existing pets. Please reassign or delete pets first."
        )

    session.delete(owner)
    session.commit()

    # No content returned for successful DELETE (HTTP 204)
    return None