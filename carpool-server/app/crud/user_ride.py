from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.models import UserRide, Ride
from ..schemas.user_ride import UserRideCreate
from .base import CRUDBase
from fastapi import HTTPException

class CRUDUserRide(CRUDBase[UserRide, UserRideCreate, UserRideCreate]):
    def create(self, db: Session, *, obj_in: UserRideCreate) -> UserRide:
        # Проверяем существование поездки
        ride = db.query(Ride).filter(Ride.ride_id == obj_in.ride_id).first()
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
            
        # Проверяем, не существует ли уже такая связь
        existing = db.query(self.model).filter(
            self.model.user_id == obj_in.user_id,
            self.model.ride_id == obj_in.ride_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="User is already associated with this ride"
            )

        db_obj = UserRide(
            user_id=obj_in.user_id,
            ride_id=obj_in.ride_id,
            role=obj_in.role
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_user_rides(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[UserRide]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_ride_users(
        self, db: Session, ride_id: int, skip: int = 0, limit: int = 100
    ) -> List[UserRide]:
        return (
            db.query(self.model)
            .filter(self.model.ride_id == ride_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def remove(
        self, db: Session, *, user_id: int, ride_id: int
    ) -> bool:
        obj = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.ride_id == ride_id
        ).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

user_ride = CRUDUserRide(UserRide) 