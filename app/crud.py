from sqlalchemy.orm import Session
from app.models import Message
from app.schemas import MessageCreate

def get_messages(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Message).offset(skip).limit(limit).all()

def create_message(db: Session, message: MessageCreate):
    db_message = Message(content=message.content, author=message.author)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message