# Инструкция по добавлению новой функциональности в Carpooling Server

## Содержание

1. [Создание модели данных](#1-создание-модели-данных)
2. [Создание схем Pydantic](#2-создание-схем-pydantic)
3. [Создание CRUD операций](#3-создание-crud-операций)
4. [Создание API эндпоинтов](#4-создание-api-эндпоинтов)
5. [Регистрация роутера](#5-регистрация-роутера)
6. [Пример полного процесса](#6-пример-полного-процесса)

## 1. Создание модели данных

### 1.1. Добавьте новую модель в `app/models/models.py`

Пример создания модели:

```python
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Poppy(Base):
    __tablename__ = "poppies"
    poppy_id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    is_blooming = Column(Boolean, default=False)

    owner = relationship("User", back_populates="poppies")
```

## 2. Создание схем Pydantic

### 2.1. Добавьте схемы в `app/schemas/poppy.py`

Пример создания схем:

```python
from pydantic import BaseModel

class PoppyBase(BaseModel):
    name: str
    color: str
    is_blooming: bool

class PoppyCreate(PoppyBase):
    owner_id: int

class PoppyResponse(PoppyBase):
    poppy_id: int
    owner_id: int

    class Config:
        from_attributes = True
```

## 3. Создание CRUD операций

### 3.1. Добавьте CRUD операции в `app/crud/poppy.py`

Пример создания CRUD операций:

```python
from typing import List
from sqlalchemy.orm import Session
from ..models.models import Poppy
from ..schemas.poppy import PoppyCreate
from .base import CRUDBase

class CRUDPoppy(CRUDBase[Poppy, PoppyCreate, PoppyCreate]):
    def get_by_owner(self, db: Session, owner_id: int) -> List[Poppy]:
        return db.query(self.model).filter(self.model.owner_id == owner_id).all()

poppy = CRUDPoppy(Poppy)
```

## 4. Создание API эндпоинтов

### 4.1. Добавьте эндпоинты в `app/api/endpoints/poppies.py`

Пример создания эндпоинтов:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...crud.poppy import poppy
from ...schemas.poppy import PoppyCreate, PoppyResponse
from ...database import get_db

router = APIRouter()

@router.post("/", response_model=PoppyResponse)
def create_poppy(
    poppy_in: PoppyCreate,
    db: Session = Depends(get_db)
):
    return poppy.create(db=db, obj_in=poppy_in)

@router.get("/owner/{owner_id}", response_model=List[PoppyResponse])
def read_poppies_by_owner(
    owner_id: int,
    db: Session = Depends(get_db)
):
    poppies = poppy.get_by_owner(db, owner_id=owner_id)
    return poppies
```

## 5. Регистрация роутера

### 5.1. Зарегистрируйте роутер в `app/api/api.py`

Пример регистрации роутера:

```python
from .endpoints import poppies

api_router.include_router(poppies.router, prefix="/poppies", tags=["poppies"])
```

## 6. Пример полного процесса

### 6.1. Пример добавления функциональности для управления маками

1. Создайте модель `Poppy` в `app/models/models.py`.
2. Создайте схемы `PoppyBase`, `PoppyCreate`, и `PoppyResponse` в `app/schemas/poppy.py`.
3. Создайте CRUD операции в `app/crud/poppy.py`.
4. Создайте эндпоинты в `app/api/endpoints/poppies.py`.
5. Зарегистрируйте роутер в `app/api/api.py`.

Теперь вы можете управлять маками через API, используя созданные эндпоинты.
