from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...crud.role import role, user_role
from ...schemas.role import (
    RoleCreate, 
    RoleResponse, 
    UserRoleCreate, 
    UserRoleResponse
)
from ...database import get_db

router = APIRouter()

@router.post("/", response_model=RoleResponse)
def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db)
):
    """Create new role"""
    db_role = role.get_by_name(db, role_name=role_in.role_name)
    if db_role:
        raise HTTPException(
            status_code=400,
            detail="Role already exists"
        )
    return role.create(db=db, obj_in=role_in)

@router.get("/", response_model=List[RoleResponse])
def read_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all roles"""
    roles = role.get_multi(db, skip=skip, limit=limit)
    return roles

@router.get("/user/{user_id}", response_model=List[RoleResponse])
def read_user_roles(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all roles for specific user"""
    roles = role.get_user_roles(db, user_id=user_id)
    return roles

@router.post("/assign", response_model=UserRoleResponse)
def assign_role(
    user_role_in: UserRoleCreate,
    db: Session = Depends(get_db)
):
    """Assign role to user"""
    return user_role.create(db=db, obj_in=user_role_in)

@router.delete("/user/{user_id}/role/{role_id}")
def remove_role(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db)
):
    """Remove role from user"""
    success = user_role.remove(db, user_id=user_id, role_id=role_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="User role not found"
        )
    return {"message": "Successfully removed"} 