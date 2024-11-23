# Импортируем FastAPI для создания веб-приложения
from fastapi import FastAPI
# Импортируем движок базы данных
from .database import engine
# Импортируем модели для работы с базой данных
from .models import models
# Импортируем настройки приложения
from .config import settings
# Импортируем API роутер
from .api.api import api_router
# Импортируем middleware для настройки CORS
from .middleware import setup_cors


# Создаем все таблицы в базе данных на основе моделей
models.Base.metadata.create_all(bind=engine)

# Создаем экземпляр FastAPI приложения с указанием названия из настроек
app = FastAPI(title=settings.PROJECT_NAME)

# Настраиваем CORS
setup_cors(app)

# Включаем API роутер в приложение
app.include_router(api_router, prefix="/api")

# Корневой маршрут, возвращает приветственное сообщение
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Маршрут с параметром, приветствует пользователя по имени
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


