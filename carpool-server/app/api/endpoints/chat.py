from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...crud.chat import chat
from ...schemas.chat import ChatMessageCreate, ChatMessageResponse
from ...database import get_db

router = APIRouter()

@router.post("/", response_model=ChatMessageResponse)
def create_message(
    message_in: ChatMessageCreate,
    sender_id: int,  # В реальном приложении это должно приходить из токена авторизации
    db: Session = Depends(get_db)
):
    """Send new message"""
    return chat.create(db=db, obj_in=message_in, sender_id=sender_id)

@router.get("/booking/{booking_id}", response_model=List[ChatMessageResponse])
def read_booking_messages(
    booking_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all messages for specific booking"""
    messages = chat.get_booking_messages(
        db, booking_id=booking_id, skip=skip, limit=limit
    )
    return messages

@router.get("/user/{user_id}", response_model=List[ChatMessageResponse])
def read_user_messages(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all messages sent by user"""
    messages = chat.get_user_messages(
        db, user_id=user_id, skip=skip, limit=limit
    )
    return messages 