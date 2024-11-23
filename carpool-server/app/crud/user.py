from typing import Optional, List
from sqlalchemy.orm import Session
from ..models.models import User, Car
from ..schemas.user import UserCreate
from .base import CRUDBase
from ..utils.security import get_password_hash

class CRUDUser(CRUDBase[User, UserCreate, UserCreate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def create(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            name=obj_in.name,
            surname=obj_in.surname,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Add car if provided
        if obj_in.car:
            car_data = obj_in.car
            car_obj = Car(
                user_id=db_obj.id,
                make=car_data.make,
                model=car_data.model,
                year=car_data.year,
                plate_number=car_data.plate_number
            )
            db.add(car_obj)
            db.commit()
            db.refresh(car_obj)

        return db_obj
    
    def get_active_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()

    def delete(self, db: Session, user_id: int) -> Optional[User]:
        """Delete a user by ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return user
        return None

user = CRUDUser(User)