from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext

from server.models.user import *

from server.security import get_current_user, check_user_admin

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/{username}", response_description="User retrieved")
async def get_user(username: str, is_admin: bool = Depends(check_user_admin)) -> User:        
    user = await User.find_one(User.username == username)
    return user


@router.get("/", response_description="Users retrieved")
async def get_users(is_admin: bool = Depends(check_user_admin)) -> list[User]:
    users = await User.find_all().to_list()
    return users

@router.put("/{username}", response_description= "User updated")
async def update_user(username: str, req: UpdateUser, is_admin: bool = Depends(check_user_admin)) -> User:
    if req.email is not None:
        existing_email = await User.find_one(User.email == req.email)
        if existing_email:
            return {"message": "User could not be updated"}

    req = {k: v for k, v in req.dict().items() if v is not None}
    update_query = {"$set":{
        field: value for field, value in req.items()
    }}

    user = await User.find_one(User.username == username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    await user.update(update_query)        
    return user

@router.delete("/{username}", response_description="User deleted")
async def delete_user(username: str, is_admin: bool = Depends(check_user_admin)) -> dict:
    user = await User.find_one(User.username == username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    await user.delete()
    return {
        "message": "User deleted successfully"
    }

@router.get("/self/")
async def get_self_data(user: User = Depends(get_current_user)):
    user_data = user.dict()
    user_out = UserOut(**user_data)
    return user_out

@router.put("/self/update/")
async def update_self_data(req: UpdateUser, user: User = Depends(get_current_user)):
    if req.email is not None:
        existing_email = await User.find_one(User.email == req.email)
        if existing_email:
            return {"message": "User could not be updated"}
        
    req = {k: v for k, v in req.dict().items() if v is not None}
    update_query = {"$set":{
        field: value for field, value in req.items()
    }}

    await user.update(update_query)
    return user