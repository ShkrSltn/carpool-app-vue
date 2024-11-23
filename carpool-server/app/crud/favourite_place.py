from typing import List
from sqlalchemy.orm import Session
from ..models.models import FavouritePlace
from ..schemas.favourite_place import FavouritePlaceCreate
from .base import CRUDBase
from fastapi import HTTPException

class CRUDFavouritePlace(CRUDBase[FavouritePlace, FavouritePlaceCreate, FavouritePlaceCreate]):
    def create(self, db: Session, *, obj_in: FavouritePlaceCreate, user_id: int) -> FavouritePlace:
        # Проверяем количество уже сохраненных мест
        existing_count = db.query(self.model).filter(
            self.model.user_id == user_id
        ).count()
        
        if existing_count >= 10:  # Ограничение на количество избранных мест
            raise HTTPException(
                status_code=400,
                detail="Maximum number of favourite places (10) reached"
            )

        db_obj = FavouritePlace(
            **obj_in.dict(),
            user_id=user_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_user_places(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[FavouritePlace]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def remove(self, db: Session, *, place_id: int, user_id: int) -> bool:
        obj = db.query(self.model).filter(
            self.model.favourite_place_id == place_id,
            self.model.user_id == user_id
        ).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

favourite_place = CRUDFavouritePlace(FavouritePlace) 