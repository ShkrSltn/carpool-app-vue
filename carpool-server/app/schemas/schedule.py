from pydantic import BaseModel, validator
from datetime import time, datetime
from typing import Optional

class UserScheduleBase(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time
    
    @validator('day_of_week')
    def validate_day_of_week(cls, v):
        if not 0 <= v <= 6:
            raise ValueError('day_of_week must be between 0 and 6')
        return v
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class UserScheduleCreate(UserScheduleBase):
    pass

class UserScheduleResponse(UserScheduleBase):
    schedule_id: int
    user_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True 