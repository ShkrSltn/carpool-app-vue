# Импортируем create_engine для создания подключения к базе данных
from sqlalchemy import create_engine
# Импортируем declarative_base для создания базового класса моделей
from sqlalchemy.ext.declarative import declarative_base
# Импортируем sessionmaker для создания сессий работы с БД
from sqlalchemy.orm import sessionmaker
# Импортируем настройки приложения из конфигурационного файла
from .config import settings

# Создаем движок SQLAlchemy для работы с базой данных
# Используем URL из настроек приложения
engine = create_engine(settings.DATABASE_URL)

# Создаем класс сессии с настройками:
# autocommit=False - автоматическая фиксация отключена
# autoflush=False - автоматическая синхронизация с БД отключена
# bind=engine - привязываем к созданному движку
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для всех моделей SQLAlchemy
Base = declarative_base()

# Функция-генератор для получения сессии БД
def get_db():
    # Создаем новую сессию
    db = SessionLocal()
    try:
        # Возвращаем сессию
        yield db
    finally:
        # Гарантированно закрываем сессию после использования
        db.close()
