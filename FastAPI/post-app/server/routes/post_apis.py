from fastapi import APIRouter, Depends

from datetime import datetime

from server.models.post import *
from server.models.user import User

from server.security import get_current_user

router = APIRouter()

@router.post("/create")
async def create_post(post_create: PostCreate, user: User = Depends(get_current_user)):
    try:
        post_create.username = user.username
        post_data = post_create.dict()
        post = Post(**post_data)
        await post.create()
        return {"message": "Post created"}
    except:
        return {"message": "Post could not be created"}
    
@router.get("/{post_id}")
async def get_post(post_id: str):
    post = await Post.get(post_id)
    return post

@router.get("/", response_description="Posts retrieved")
async def get_users() -> list[Post]:
    posts = await Post.find_all().to_list()
    return posts