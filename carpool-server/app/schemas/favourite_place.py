from pydantic import BaseModel
from datetime import datetime

class FavouritePlaceCreate(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float

class FavouritePlaceResponse(BaseModel):
    favourite_place_id: int
    user_id: int
    name: str
    address: str
    latitude: float
    longitude: float
    created_at: datetime

    class Config:
        from_attributes = True 