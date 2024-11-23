from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        # Получение одной записи по id
        return db.query(self.model).filter(self.model.ride_id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        # Получение списка записей с пагинацией
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        # Создание новой записи в базе данных
        obj_in_data = obj_in.dict()  # Преобразование входных данных в словарь
        db_obj = self.model(**obj_in_data)  # Создание объекта модели
        db.add(db_obj)  # Добавление объекта в сессию
        db.commit()  # Сохранение изменений
        db.refresh(db_obj)  # Обновление объекта из базы данных
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        # Обновление существующей записи
        obj_data = db_obj.__dict__  # Получение текущих данных объекта
        if isinstance(obj_in, dict):  # Проверка типа входных данных
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)  # Получение только установленных полей
        
        # Обновление полей объекта
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)  # Добавление обновленного объекта в сессию
        db.commit()  # Сохранение изменений
        db.refresh(db_obj)  # Обновление объекта из базы данных
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        # Удаление записи по id
        obj = db.query(self.model).get(id)  # Получение объекта
        db.delete(obj)  # Удаление объекта
        db.commit()  # Сохранение изменений
        return obj