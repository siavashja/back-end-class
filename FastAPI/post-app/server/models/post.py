from datetime import datetime

from beanie import Document
from pydantic import BaseModel
from typing import Optional

class Post(Document):

    username: str
    caption: str

    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Settings:

        name = "post"

    class Config:
        schema_extra = {
            "example": {
                "username": "Siavash",
                "caption": "Hi",
                "created_at": "2023-07-09T11:01:07.574600",
                "updated_at": "2023-07-09T11:01:07.574600",
            }
        }

class PostCreate(BaseModel):

    username: Optional[str]
    caption: Optional[str]

    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()