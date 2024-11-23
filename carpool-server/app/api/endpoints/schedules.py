from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...crud.schedule import schedule
from ...schemas.schedule import UserScheduleCreate, UserScheduleResponse
from ...database import get_db
from ...utils.security import get_current_user
from ...models.models import User

router = APIRouter()

@router.post("/", response_model=UserScheduleResponse)
def create_schedule(
    schedule_in: UserScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new schedule for current user or update if exists"""
    try:
        return schedule.create(db=db, obj_in=schedule_in, user_id=current_user.id)
    except HTTPException as e:
        if e.status_code == 400 and "already exists" in str(e.detail):
            # Get existing schedule
            existing = db.query(schedule.model).filter(
                schedule.model.user_id == current_user.id,
                schedule.model.day_of_week == schedule_in.day_of_week,
                schedule.model.is_active == True
            ).first()
            
            # Update existing schedule
            return schedule.update_schedule(
                db=db,
                schedule_id=existing.schedule_id,
                user_id=current_user.id,
                obj_in=schedule_in
            )
        raise e

@router.get("/me", response_model=List[UserScheduleResponse])
def read_my_schedule(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's schedule"""
    return schedule.get_user_schedule(db, user_id=current_user.id)

@router.put("/{schedule_id}", response_model=UserScheduleResponse)
def update_schedule(
    schedule_id: int,
    schedule_in: UserScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update specific schedule entry"""
    return schedule.update_schedule(
        db=db, 
        schedule_id=schedule_id, 
        user_id=current_user.id,
        obj_in=schedule_in
    ) 