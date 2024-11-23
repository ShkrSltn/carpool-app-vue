from pydantic import BaseModel
from .enums import UserRolesEnum
from typing import List

class RoleCreate(BaseModel):
    role_name: UserRolesEnum

class RoleResponse(BaseModel):
    role_id: int
    role_name: UserRolesEnum

    class Config:
        from_attributes = True

class UserRoleCreate(BaseModel):
    user_id: int
    role_id: int

class UserRoleResponse(BaseModel):
    user_id: int
    role_id: int
    role_name: UserRolesEnum

    class Config:
        from_attributes = True 