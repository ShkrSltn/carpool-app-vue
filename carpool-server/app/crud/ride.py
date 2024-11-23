from typing import List, Optional  # Импортируем типы для аннотаций: список и необязательный тип
from sqlalchemy.orm import Session  # Импортируем класс Session из SQLAlchemy для работы с сессиями базы данных
from ..models.models import Ride  # Импортируем модель Ride из модуля models
from ..schemas.ride import RideCreate  # Обновленный импорт
from .base import CRUDBase  # Импортируем базовый класс CRUDBase из текущего пакета

class CRUDRide(CRUDBase[Ride, RideCreate, RideCreate]):  # Определяем класс CRUDRide, наследующий от CRUDBase
    def get_by_driver(self, db: Session, driver_id: int) -> List[Ride]:  # Метод для получения поездок по ID водителя
        return db.query(self.model).filter(self.model.driver_id == driver_id).all()  # Выполняем запрос к базе данных для получения всех поездок водителя

    def get_active_rides(self, db: Session, skip: int = 0, limit: int = 100) -> List[Ride]:  # Метод для получения активных поездок с возможностью пропуска и ограничения
        return db.query(self.model)\
            .filter(self.model.is_active == True)\
            .offset(skip)\
            .limit(limit)\
            .all()  # Получаем все записи, соответствующие условиям

    def delete(self, db: Session, *, ride_id: int):
        """
        Удаление поездки по её ID
        """
        db_ride = db.query(self.model).filter(self.model.ride_id == ride_id).first()
        if db_ride:
            db.delete(db_ride)
            db.commit()
            return db_ride
        return None

ride = CRUDRide(Ride)  # Создаем экземпляр CRUDRide для работы с моделью Ride
