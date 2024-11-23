from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt
from typing import Optional
from ..config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError
from ..models.models import User
from ..database import get_db

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие открытого пароля хешированному
    Args:
        plain_password: пароль в открытом виде
        hashed_password: хешированный пароль из базы данных
    Returns:
        bool: True если пароли совпадают, False если нет
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    now = datetime.utcnow()
    to_encode.update({"iat": now})
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

def get_password_hash(password: str) -> str:
    """
    Создает хеш из открытого пароля
    Args:
        password: пароль в открытом виде
    Returns:
        str: хешированный пароль
    """
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Аутентифицирует пользователя по email и паролю
    Args:
        db: сессия базы данных
        email: email пользователя
        password: пароль в открытом виде
    Returns:
        Optional[User]: объект пользователя если аутентификация успешна, None если нет
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

