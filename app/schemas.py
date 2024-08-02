
from pydantic import BaseModel

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    author: str

class MessageResponse(MessageBase):
    id: int
    author: str

    class Config:
        orm_mode = True