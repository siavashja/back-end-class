from beanie import init_beanie
import motor.motor_asyncio

from server.models.user import User
from server.models.post import Post

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017/postapp_db"
    )

    await init_beanie(database=client.postapp_db, document_models=[User, Post])