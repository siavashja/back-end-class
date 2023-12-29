from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from server.models.user import User, UserCreate

from server.security import *

router = APIRouter()

@router.post("/sign-up", response_description="User created")
async def create_user(user_create: UserCreate = Depends()):

    try:
        existing_username = await User.find_one(User.username == user_create.username)
        if existing_username:
            return {"message": "User could not be created"}
        if user_create.email is not None:
            existing_email = await User.find_one(User.email == user_create.email)
            if existing_email:
                return {"message": "User could not be created"}
        
        user_data = user_create.dict()
        user = User(**user_data)

        password = user.password
        hashed_password = pwd_context.hash(SECRET_KEY, password)
        user.password = hashed_password

        await user.create()
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        response = JSONResponse(
            {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token},
            headers={"Set-Cookie": f"refresh_token={refresh_token}; HttpOnly; Path=/; Max-Age={REFRESH_TOKEN_EXPIRE_DAYS*24*60*60}"},
        )
        return response
    except:
        return {"message": "User could not be created"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    response = JSONResponse(
        {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token},
        headers={"Set-Cookie": f"refresh_token={refresh_token}; HttpOnly; Path=/; Max-Age={REFRESH_TOKEN_EXPIRE_DAYS*24*60*60}"},
    )
    return response

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = await User.get({"username": username})
        new_access_token = create_access_token(user)
        response = JSONResponse(
            {"access_token": new_access_token, "token_type": "bearer"},
            headers={"Set-Cookie": f"refresh_token={refresh_token}; HttpOnly; Path=/; Max-Age={REFRESH_TOKEN_EXPIRE_DAYS*24*60*60}"},
        )
        return response
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")