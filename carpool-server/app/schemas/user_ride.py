from pydantic import BaseModel
from .enums import UserRolesEnum

class UserRideCreate(BaseModel):
    user_id: int
    ride_id: int
    role: UserRolesEnum

class UserRideResponse(BaseModel):
    user_id: int
    ride_id: int
    role: UserRolesEnum

    class Config:
        from_attributes = True 