from datetime import datetime

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, EmailStr

from typing import Optional

import pymongo

class User(Document):

    username: Indexed(str, unique = True, index_type=pymongo.TEXT)
    password: Optional[str]
    email: Optional[EmailStr]
    joined_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    profile_pic_path: Optional[str]

    is_superuser: bool = False

    class Settings:
        name = "user"

    class Config:
        schema_extra = {
            "example": {
                "username": "Siavash",
                "password": "12345678",
                "email": "siavash.005@gmail.com",
                "joined_at": datetime.now()
            }
        }

class UserCreate(BaseModel):
    username: str
    password: Optional[str]
    email: Optional[str]
    joined_at: datetime = datetime.now()

    class Settings:
        name = "user"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "Siavash",
                "password": "12345678",
                "email": "siavash.005@gmail.com",
                "joined_at": datetime.now()
            }
        }

class UpdateUser(BaseModel):
    updated_at: Optional[datetime]
    email: Optional[str]

    class Config:
        json_encoders = {PydanticObjectId: str}
        schema_extra = {
            "example": {
                "email": "siavash.005@gmail.com",
                "updated_at": datetime.now()
            }
        }

class UserOut(BaseModel):

    username: str
    email: Optional[str]
    joined_at: datetime
    updated_at: datetime