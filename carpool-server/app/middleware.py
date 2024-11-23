from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",    # Vue dev server
            "http://127.0.0.1:5173",    # Альтернативный адрес Vue
            "http://localhost:8000",    # FastAPI
            "http://127.0.0.1:8000",    # Альтернативный адрес FastAPI
        ],
        allow_credentials=True,
        allow_methods=["*"],           # Разрешаем все методы
        allow_headers=["*"],           # Разрешаем все заголовки
        expose_headers=["*"],
        max_age=600,                   # Кэширование CORS на 10 минут
    ) 