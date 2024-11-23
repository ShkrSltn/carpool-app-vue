from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.models import UserSchedule
from ..schemas.schedule import UserScheduleCreate
from .base import CRUDBase

class CRUDUserSchedule(CRUDBase[UserSchedule, UserScheduleCreate, UserScheduleCreate]):
    def create(self, db: Session, *, obj_in: UserScheduleCreate, user_id: int) -> UserSchedule:
        # Проверяем, нет ли уже расписания на этот день
        existing = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.day_of_week == obj_in.day_of_week,
            self.model.is_active == True
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Schedule for day {obj_in.day_of_week} already exists"
            )

        db_obj = UserSchedule(
            user_id=user_id,
            day_of_week=obj_in.day_of_week,
            start_time=obj_in.start_time,
            end_time=obj_in.end_time
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_user_schedule(
        self, db: Session, user_id: int
    ) -> List[UserSchedule]:
        return (
            db.query(self.model)
            .filter(
                self.model.user_id == user_id,
                self.model.is_active == True
            )
            .order_by(self.model.day_of_week)
            .all()
        )

    def update_schedule(
        self, 
        db: Session, 
        *, 
        schedule_id: int, 
        user_id: int,
        obj_in: UserScheduleCreate
    ) -> UserSchedule:
        schedule = db.query(self.model).filter(
            self.model.schedule_id == schedule_id,
            self.model.user_id == user_id
        ).first()
        
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")
            
        schedule.day_of_week = obj_in.day_of_week
        schedule.start_time = obj_in.start_time
        schedule.end_time = obj_in.end_time
        
        db.commit()
        db.refresh(schedule)
        return schedule

schedule = CRUDUserSchedule(UserSchedule) 