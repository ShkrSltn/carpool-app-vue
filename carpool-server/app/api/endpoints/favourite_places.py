from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...crud.favourite_place import favourite_place
from ...schemas.favourite_place import FavouritePlaceCreate, FavouritePlaceResponse
from ...database import get_db

router = APIRouter()

@router.post("/user/{user_id}", response_model=FavouritePlaceResponse)
def create_favourite_place(
    user_id: int,
    place_in: FavouritePlaceCreate,
    db: Session = Depends(get_db)
):
    """Create new favourite place for user"""
    return favourite_place.create(db=db, obj_in=place_in, user_id=user_id)

@router.get("/user/{user_id}", response_model=List[FavouritePlaceResponse])
def read_user_places(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all favourite places for user"""
    places = favourite_place.get_user_places(
        db, user_id=user_id, skip=skip, limit=limit
    )
    return places

@router.delete("/{place_id}/user/{user_id}")
def delete_favourite_place(
    place_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete favourite place"""
    success = favourite_place.remove(db, place_id=place_id, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Favourite place not found"
        )
    return {"message": "Successfully removed"} 