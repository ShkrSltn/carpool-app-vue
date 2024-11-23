from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...crud.booking import booking
from ...schemas.booking import BookingCreate, BookingResponse
from ...schemas.enums import BookingStatusEnum
from ...database import get_db

router = APIRouter()

@router.post("/", response_model=BookingResponse)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db)
):
    """Create new booking"""
    return booking.create(db=db, obj_in=booking_in)

@router.get("/", response_model=List[BookingResponse])
def read_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of all bookings"""
    bookings = booking.get_multi(db, skip=skip, limit=limit)
    return bookings

@router.get("/user/{user_id}", response_model=List[BookingResponse])
def read_user_bookings(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all bookings for specific user"""
    bookings = booking.get_user_bookings(db, user_id=user_id, skip=skip, limit=limit)
    return bookings

@router.get("/ride/{ride_id}", response_model=List[BookingResponse])
def read_ride_bookings(
    ride_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all bookings for specific ride"""
    bookings = booking.get_ride_bookings(db, ride_id=ride_id, skip=skip, limit=limit)
    return bookings

@router.put("/{booking_id}/status", response_model=BookingResponse)
def update_booking_status(
    booking_id: int,
    status: BookingStatusEnum,
    db: Session = Depends(get_db)
):
    """Update booking status"""
    db_booking = booking.update_status(db, booking_id=booking_id, new_status=status)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking 