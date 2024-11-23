from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from .car import CarCreate, CarResponse

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    name: Optional[str]
    surname: Optional[str]
    car: Optional[CarCreate] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int

class UserResponse(UserBase):
    user_id: int = Field(..., alias='id')
    carbon_bonus_points: int
    created_at: datetime
    cars: Optional[List[CarResponse]] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str