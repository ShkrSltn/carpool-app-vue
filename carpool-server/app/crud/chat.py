from typing import List
from sqlalchemy.orm import Session
from ..models.models import ChatMessage, Booking
from ..schemas.chat import ChatMessageCreate
from .base import CRUDBase
from fastapi import HTTPException

class CRUDChatMessage(CRUDBase[ChatMessage, ChatMessageCreate, ChatMessageCreate]):
    def create(self, db: Session, *, obj_in: ChatMessageCreate, sender_id: int) -> ChatMessage:
        # Проверяем существование бронирования
        booking = db.query(Booking).filter(
            Booking.booking_id == obj_in.booking_id
        ).first()
        
        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )
            
        # Проверяем, что отправитель является участником бронирования
        if sender_id != booking.user_id and sender_id != booking.ride.driver_id:
            raise HTTPException(
                status_code=403,
                detail="User is not a participant of this booking"
            )

        db_obj = ChatMessage(
            booking_id=obj_in.booking_id,
            sender_id=sender_id,
            message=obj_in.message
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_booking_messages(
        self, db: Session, booking_id: int, skip: int = 0, limit: int = 100
    ) -> List[ChatMessage]:
        return (
            db.query(self.model)
            .filter(self.model.booking_id == booking_id)
            .order_by(self.model.sent_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_user_messages(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[ChatMessage]:
        return (
            db.query(self.model)
            .filter(self.model.sender_id == user_id)
            .order_by(self.model.sent_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

chat = CRUDChatMessage(ChatMessage) 