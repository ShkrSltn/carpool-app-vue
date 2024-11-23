# Импортируем APIRouter из FastAPI для создания модульных маршрутов
from fastapi import APIRouter
# Импортируем модуль rides из локальной директории endpoints
from .endpoints import rides, users, bookings, user_rides, favourite_places, chat, roles, schedules

# Создаем основной роутер API
api_router = APIRouter()

# Подключаем роутер для работы с поездками (rides)
# prefix="/rides" означает, что все маршруты будут начинаться с /rides
# tags=["rides"] используется для группировки маршрутов в документации
api_router.include_router(rides.router, prefix="/rides", tags=["rides"])

# Подключаем роутер для работы с пользователями (users)
# prefix="/users" означает, что все маршруты будут начинаться с /users
# tags=["users"] используется для группировки маршрутов в документации
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Подключаем роутер для работы с бронированиями (bookings)
# prefix="/bookings" означает, что все маршруты будут начинаться с /bookings
# tags=["bookings"] используется для группировки маршрутов в документации
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])

# Подключаем роутер для работы с поездками пользователей (user_rides)
# prefix="/user-rides" означает, что все маршруты будут начинаться с /user-rides
# tags=["user-rides"] используется для группировки маршрутов в документации
api_router.include_router(user_rides.router, prefix="/user-rides", tags=["user-rides"])

# Подключаем роутер для работы с избранными местами (favourite_places)
# prefix="/favourite-places" означает, что все маршруты будут начинаться с /favourite-places
# tags=["favourite-places"] используется для группировки маршрутов в документации
api_router.include_router(
    favourite_places.router, 
    prefix="/favourite-places", 
    tags=["favourite-places"]
)

# Подключаем роутер для работы с чатом (chat)
# prefix="/chat" означает, что все маршруты будут начинаться с /chat
# tags=["chat"] используется для группировки маршрутов в документации
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

# Подключаем роутер для работы с ролями (roles)
# prefix="/roles" означает, что все маршруты будут начинаться с /roles
# tags=["roles"] используется для группировки маршрутов в документации
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])

# Подключаем роутер для работы с расписаниями (schedules)
# prefix="/schedules" означает, что все маршруты будут начинаться с /schedules
# tags=["schedules"] используется для группировки маршрутов в документации
api_router.include_router(
    schedules.router,
    prefix="/schedules",
    tags=["schedules"]
)

# Добавьте другие роутеры здесь по мере их создания