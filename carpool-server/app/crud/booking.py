from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.models import Booking, Ride
from ..schemas.booking import BookingCreate
from .base import CRUDBase
from ..schemas.enums import BookingStatusEnum
from fastapi import HTTPException

class CRUDBooking(CRUDBase[Booking, BookingCreate, BookingCreate]):
    def create(self, db: Session, *, obj_in: BookingCreate) -> Booking:
        # Check if ride exists and has enough seats
        ride = db.query(Ride).filter(Ride.ride_id == obj_in.ride_id).first()
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        if ride.available_seats < obj_in.seats_count:
            raise HTTPException(status_code=400, detail="Not enough available seats")

        # Create booking
        db_obj = Booking(
            ride_id=obj_in.ride_id,
            user_id=obj_in.user_id,
            seats_count=obj_in.seats_count,
            status=BookingStatusEnum.requested
        )
        db.add(db_obj)
        
        # Update available seats
        ride.available_seats -= obj_in.seats_count
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_user_bookings(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Booking]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_ride_bookings(
        self, db: Session, ride_id: int, skip: int = 0, limit: int = 100
    ) -> List[Booking]:
        return (
            db.query(self.model)
            .filter(self.model.ride_id == ride_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_status(
        self, db: Session, booking_id: int, new_status: BookingStatusEnum
    ) -> Optional[Booking]:
        booking = db.query(self.model).filter(self.model.booking_id == booking_id).first()
        if booking:
            # If canceling or rejecting, return seats to ride
            if new_status in [BookingStatusEnum.canceled, BookingStatusEnum.rejected] and \
               booking.status not in [BookingStatusEnum.canceled, BookingStatusEnum.rejected]:
                ride = db.query(Ride).filter(Ride.ride_id == booking.ride_id).first()
                if ride:
                    ride.available_seats += booking.seats_count
            
            booking.status = new_status
            db.commit()
            db.refresh(booking)
        return booking

booking = CRUDBooking(Booking) 