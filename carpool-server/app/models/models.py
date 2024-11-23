from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text, Time
# Импортируем необходимые классы из SQLAlchemy для определения столбцов и их типов

from sqlalchemy.orm import relationship
# Импортируем функцию relationship для установления связей между таблицами

from datetime import datetime
# Импортируем datetime для работы с датой и временем

from ..database import Base
# Импортируем базовый класс для моделей из модуля database

from ..schemas.enums import UserRolesEnum, BookingStatusEnum  # Обновленный импорт

class User(Base):
    # Определяем модель пользователя, наследуемую от Base
    __tablename__ = "users"
    # Указываем имя таблицы в базе данных
    id = Column(Integer, primary_key=True, index=True)
    # Определяем столбец id как первичный ключ и индекс
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    # Определяем столбец для имени пользователя, не может быть пустым
    email = Column(String, unique=True, nullable=False)
    # Определяем столбец для email, должен быть уникальным и не пустым
    hashed_password = Column(String, nullable=False)
    # Определяем столбец для хэшированного пароля, не может быть пустым
    carbon_bonus_points = Column(Integer, default=0)
    # Определяем столбец для бонусных баллов, по умолчанию 0
    created_at = Column(DateTime, default=datetime.utcnow)
    # Определяем столбец для даты создания, по умолчанию текущее время
    is_active = Column(Boolean, default=True)
    # Определяем столбец для статуса активности, по умолчанию активен
    cars = relationship("Car", back_populates="user", cascade="all, delete-orphan")
    last_logout = Column(DateTime, nullable=True)

    roles = relationship("UserRole", back_populates="user")
    # Устанавливаем связь с таблицей UserRole
    favourite_places = relationship("FavouritePlace", back_populates="user")
    # Устанавливаем связь с таблицей FavouritePlace
    user_rides = relationship("UserRide", back_populates="user")
    # Устанавливаем связь с таблицей UserRide
    user_bookings = relationship("UserBooking", back_populates="user")
    driver_rides = relationship("Ride", foreign_keys="[Ride.driver_id]", back_populates="driver")
    schedules = relationship("UserSchedule", back_populates="user", cascade="all, delete-orphan")

class Role(Base):
    # Определяем модель роли, наследуемую от Base
    __tablename__ = "roles"
    # Указываем имя таблицы в базе данных
    role_id = Column(Integer, primary_key=True, index=True)
    # Определяем столбец role_id как первичный ключ и индекс
    role_name = Column(Enum(UserRolesEnum), unique=True, nullable=False)
    # Определяем столбец для имени роли, должен быть уникальным и не пустым

    users = relationship("UserRole", back_populates="role")
    # Устанавливаем связь с таблицей UserRole

class UserRole(Base):
    # Определяем модель связи пользователя и роли, наследуемую от Base
    __tablename__ = "user_roles"
    # Указываем имя таблицы в базе данных
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    # Определяем столбец user_id как первичный ключ и внешний ключ на таблицу users
    role_id = Column(Integer, ForeignKey("roles.role_id"), primary_key=True)
    # Определяем столбец role_id как первичный ключ и внешний ключ на таблицу roles

    user = relationship("User", back_populates="roles")
    # Устанавливаем связь с таблицей User
    role = relationship("Role", back_populates="users")
    # Устанавливаем связь с таблицей Role

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    plate_number = Column(String, unique=True, nullable=False)

    user = relationship("User", back_populates="cars")
class Ride(Base):
    # Определяем модель поездки, наследуемую от Base
    __tablename__ = "rides"
    # Указываем имя таблицы в базе данных
    ride_id = Column(Integer, primary_key=True, index=True)
    # Определяем столбец ride_id как первичный ключ и индекс
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Определяем столбец driver_id как внешний ключ на таблицу users, не может быть пустым
    origin = Column(String, nullable=False)
    # Определяем столбец для места отправления, не может быть пустым
    origin_latitude = Column(Float, nullable=False)
    # Определяем столбец для широты места отравления, не может быть пустым
    origin_longitude = Column(Float, nullable=False)
    # Определяем столбец для долготы места отправления, не может быть пустым
    destination = Column(String, nullable=False)
    # Определяем столбец для места назначения, не может быть пустым
    destination_latitude = Column(Float, nullable=False)
    # Определяем столбец для широты места назначения, не может быть пустым
    destination_longitude = Column(Float, nullable=False)
    # Определяем столбец для долготы места назначения, не может быть пустым
    departure_time = Column(DateTime, nullable=False)
    # Определяем столбец для времени отправления, не может быть пустым
    available_seats = Column(Integer, nullable=False)
    # Определяем столбец для количества доступных мест, не может быть пустым
    is_active = Column(Boolean, default=True)
    # Определяем столбец для статуса активности поездки, по умолчанию активна
    created_at = Column(DateTime, default=datetime.utcnow)
    # Определяем столбец для даты создания, по умолчанию текущее время

    driver = relationship("User", foreign_keys=[driver_id], back_populates="driver_rides")
    bookings = relationship("Booking", back_populates="ride")
    user_rides = relationship("UserRide", back_populates="ride")

class UserRide(Base):
    # Определяем модель связи пользователя и поездки, наследуемую от Base
    __tablename__ = "user_rides"
    # Указываем имя таблицы в базе данных
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    # Определяем столбец user_id как первичный ключ и внешний ключ на таблицу users
    ride_id = Column(Integer, ForeignKey("rides.ride_id"), primary_key=True)
    # Определяем столбец ride_id как первичный ключ и внешний ключ на таблицу rides
    role = Column(Enum(UserRolesEnum), nullable=False)
    # Определяем столбец для роли пользователя в поездке, не может быть пустым

    user = relationship("User", back_populates="user_rides")
    # Устанавливаем связь с таблицей User
    ride = relationship("Ride", back_populates="user_rides")
    # Устанавливаем связь с таблицей Ride

class Booking(Base):
    # Определяем модель бронирования, наследуемую от Base
    __tablename__ = "bookings"
    # Указываем имя таблицы в базе данных
    booking_id = Column(Integer, primary_key=True, index=True)
    # Определяем столбец booking_id как первичный ключ и индекс
    ride_id = Column(Integer, ForeignKey("rides.ride_id"), nullable=False)
    # Определяем столбец ride_id как внешний ключ на таблицу rides, не может быть пустым
    request_time = Column(DateTime, default=datetime.utcnow)
    # Определяем столбец для времени запроса, по умолчанию текущее время
    status = Column(Enum(BookingStatusEnum), default=BookingStatusEnum.requested)
    # Определяем столбец для статуса бронирования, по умолчанию "запрошено"

    ride = relationship("Ride", back_populates="bookings")
    # Устанавливаем связь с таблицей Ride
    user_bookings = relationship("UserBooking", back_populates="booking")
    # Устанавливаем связь с таблицей UserBooking
    chat_messages = relationship("ChatMessage", back_populates="booking")

class UserBooking(Base):
    # Определяем модель связи пользователя и бронирования, наследуемую от Base
    __tablename__ = "user_bookings"
    # Указываем имя таблицы в базе данных
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    # Определяем столбец user_id как первичный ключ и внешний ключ на таблицу users
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), primary_key=True)
    # Определяем столбец booking_id как первичный ключ и внешний ключ на таблицу bookings
    role = Column(Enum(UserRolesEnum), nullable=False)
    # Определяем столбец для роли пользователя в бронировании, не может быть пустым

    user = relationship("User", back_populates="user_bookings")
    # Устанавливаем связь с таблицей User
    booking = relationship("Booking", back_populates="user_bookings")
    # Устанавливаем связь с таблицей Booking

class ChatMessage(Base):
    # Определяем модель сообщения в чате, наследуемую от Base
    __tablename__ = "chat_messages"
    # Указываем имя таблицы в базе данных
    message_id = Column(Integer, primary_key=True, index=True)
    # Определяем столбец message_id как первичный ключ и индекс
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), nullable=False)
    # Определяем столбец booking_id как внешний ключ на таблицу bookings, не может быть пустым
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Определяем столбец sender_id как внешний ключ на таблицу users, не может быть пустым
    message = Column(Text, nullable=False)
    # Определяем столбец для текста сообщения, не может быть пустым
    sent_at = Column(DateTime, default=datetime.utcnow)
    # Определяем столбец для времени отправки, по умолчанию текущее время

    booking = relationship("Booking", back_populates="chat_messages")
    # Устанавливаем связь с таблицей Booking
    sender = relationship("User")
    # Устанавливаем связь с таблицей User

class FavouritePlace(Base):
    # Определяем модель избранного места, наследуемую от Base
    __tablename__ = "favourite_places"
    # Указываем имя таблицы в базе данных
    favourite_place_id = Column(Integer, primary_key=True, index=True)
    # Определяем столбец favourite_place_id как первичный ключ и индекс
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Определяем столбец user_id как внешний ключ на таблицу users, не может быть пустым
    name = Column(String, nullable=False)
    # Определяем столбец для имени места, не может быть пустым
    address = Column(String, nullable=False)
    # Определяем столбец для адреса места, не может быть пустым
    latitude = Column(Float, nullable=False)
    # Определяем столбец для широты места, не может быть пустым
    longitude = Column(Float, nullable=False)
    # Определяем столбец для долготы места, не может быть пустым
    created_at = Column(DateTime, default=datetime.utcnow)
    # Определяем столбец для даты создания, по умолчанию текущее время

    user = relationship("User", back_populates="favourite_places")
    # Устанавливаем связь с таблицей User

class UserSchedule(Base):
    __tablename__ = "user_schedules"
    
    schedule_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0-6 (Понедельник-Воскресенье)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="schedules")