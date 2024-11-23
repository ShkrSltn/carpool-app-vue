from pydantic import BaseModel
from datetime import datetime
from .enums import BookingStatusEnum

class BookingCreate(BaseModel):
    ride_id: int
    user_id: int
    seats_count: int = 1

class BookingResponse(BaseModel):
    booking_id: int
    ride_id: int
    request_time: datetime
    status: BookingStatusEnum
    user_id: int
    seats_count: int

    class Config:
        from_attributes = True 