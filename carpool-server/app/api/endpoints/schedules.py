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
    """Create new schedule for current user"""
    return schedule.create(db=db, obj_in=schedule_in, user_id=current_user.id)

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