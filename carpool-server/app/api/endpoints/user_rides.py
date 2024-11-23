from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...crud.user_ride import user_ride
from ...schemas.user_ride import UserRideCreate, UserRideResponse
from ...database import get_db

router = APIRouter()

@router.post("/", response_model=UserRideResponse)
def create_user_ride(
    user_ride_in: UserRideCreate,
    db: Session = Depends(get_db)
):
    """Associate user with ride in specific role"""
    return user_ride.create(db=db, obj_in=user_ride_in)

@router.get("/user/{user_id}", response_model=List[UserRideResponse])
def read_user_rides(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all rides associated with user"""
    rides = user_ride.get_user_rides(db, user_id=user_id, skip=skip, limit=limit)
    return rides

@router.get("/ride/{ride_id}", response_model=List[UserRideResponse])
def read_ride_users(
    ride_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all users associated with ride"""
    users = user_ride.get_ride_users(db, ride_id=ride_id, skip=skip, limit=limit)
    return users

@router.delete("/{user_id}/{ride_id}")
def delete_user_ride(
    user_id: int,
    ride_id: int,
    db: Session = Depends(get_db)
):
    """Remove user from ride"""
    success = user_ride.remove(db, user_id=user_id, ride_id=ride_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="User ride association not found"
        )
    return {"message": "Successfully removed"} 