# Импорт необходимых компонентов из FastAPI и других модулей
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...crud.ride import ride
from ...schemas.ride import RideCreate, RideResponse
from ...database import get_db
from ...models.models import User

# Создание роутера для обработки запросов
router = APIRouter()

@router.post("/", response_model=RideResponse)
def create_ride(
    ride_in: RideCreate,  # Входные данные для создания поездки
    db: Session = Depends(get_db)  # Получение сессии БД через dependency injection
):
    """Создание новой поездки"""
    # Verify that the driver exists
    driver = db.query(User).filter(User.id == ride_in.driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )
    return ride.create(db=db, obj_in=ride_in)

@router.get("/", response_model=List[RideResponse])
def read_rides(
    skip: int = 0,  # Параметр пагинации: сколько записей пропустить
    limit: int = 100,  # Параметр пагинации: сколько записей вернуть
    db: Session = Depends(get_db)  # Получение сессии БД
):
    """Получение списка всех поездок с пагинацией"""
    rides = ride.get_multi(db, skip=skip, limit=limit)
    return rides

@router.get("/active", response_model=List[RideResponse])
def read_active_rides(
    skip: int = 0,  # Параметр пагинации: сколько записей пропустить
    limit: int = 100,  # Параметр пагинации: сколько записей вернуть
    db: Session = Depends(get_db)  # Получение сессии БД
):
    """Получение списка только активных поездок"""
    rides = ride.get_active_rides(db, skip=skip, limit=limit)
    return rides

@router.get("/{ride_id}", response_model=RideResponse)
def read_ride(
    ride_id: int,  # ID поездки для получения
    db: Session = Depends(get_db)  # Получение сессии БД
):
    """Получение информации о конкретной поездке по её ID"""
    db_ride = ride.get(db, id=ride_id)
    if db_ride is None:
        # Если поездка не найдена, возвращаем ошибку 404
        raise HTTPException(status_code=404, detail="Ride not found")
    return db_ride


@router.delete("/{ride_id}", response_model=RideResponse)
def delete_ride(
        ride_id: int,  # ID поездки для удаления
        db: Session = Depends(get_db)  # Получение сессии БД
):
    """
    Удаление поездки по её ID
    """
    # Получаем поездку из базы данных
    db_ride = db.query(ride.model).filter(ride.model.ride_id == ride_id).first()
    if db_ride is None:
        # Если поездка не найдена, возвращаем ошибку 404
        raise HTTPException(status_code=404, detail="Ride not found")

    # Удаляем поездку
    db.delete(db_ride)
    db.commit()
    return db_ride
