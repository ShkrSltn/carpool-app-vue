from pydantic import BaseModel
from datetime import datetime

class ChatMessageCreate(BaseModel):
    booking_id: int
    message: str

class ChatMessageResponse(BaseModel):
    message_id: int
    booking_id: int
    sender_id: int
    message: str
    sent_at: datetime

    class Config:
        from_attributes = True 