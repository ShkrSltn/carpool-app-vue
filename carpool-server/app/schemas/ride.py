from pydantic import BaseModel
from datetime import datetime

class RideBase(BaseModel):
    origin: str
    origin_latitude: float
    origin_longitude: float
    destination: str
    destination_latitude: float
    destination_longitude: float
    departure_time: datetime
    available_seats: int

class RideCreate(RideBase):
    driver_id: int

class RideResponse(RideBase):
    ride_id: int
    driver_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True 