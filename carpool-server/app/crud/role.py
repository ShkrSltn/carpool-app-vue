from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.models import Role, UserRole
from ..schemas.role import RoleCreate, UserRoleCreate
from .base import CRUDBase
from fastapi import HTTPException

class CRUDRole(CRUDBase[Role, RoleCreate, RoleCreate]):
    def get_by_name(self, db: Session, role_name: str) -> Optional[Role]:
        return db.query(self.model).filter(self.model.role_name == role_name).first()

    def get_user_roles(self, db: Session, user_id: int) -> List[Role]:
        return (
            db.query(self.model)
            .join(UserRole)
            .filter(UserRole.user_id == user_id)
            .all()
        )

class CRUDUserRole(CRUDBase[UserRole, UserRoleCreate, UserRoleCreate]):
    def create(self, db: Session, *, obj_in: UserRoleCreate) -> UserRole:
        # Проверяем, не существует ли уже такая роль у пользователя
        existing = db.query(self.model).filter(
            self.model.user_id == obj_in.user_id,
            self.model.role_id == obj_in.role_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=400,
                detail="User already has this role"
            )

        db_obj = UserRole(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, user_id: int, role_id: int) -> bool:
        obj = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.role_id == role_id
        ).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

role = CRUDRole(Role)
user_role = CRUDUserRole(UserRole) 