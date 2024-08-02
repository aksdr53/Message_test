from fastapi import FastAPI, Depends
from app.models import Message
from app.database import get_db
from app.crud import get_messages, create_message
from app.schemas import MessageCreate, MessageResponse
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/api/v1/messages/", response_model=list[MessageResponse])
def read_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    messages = get_messages(db, skip=skip, limit=limit)
    return messages

@app.post("/api/v1/message/", response_model=MessageResponse)
def write_message(message: MessageCreate, db: Session = Depends(get_db)):
    return create_message(db=db, message=message)