from datetime import datetime,timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from starlette.requests import Request

from .secret import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from server.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(user: User):
    to_encode = {"sub": user.username}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(user: User):
    to_encode = {"sub": user.username}
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str):
    user = await User.find_one(User.username == username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username or password is incorrect.")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is incorrect.")
    return user

async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires_at = datetime.fromtimestamp(payload.get("exp"))
        if datetime.utcnow() > expires_at:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return await User.find_one(User.username == username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

async def get_refresh_token(request: Request):
    cookies = request.cookies
    refresh_token = cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return refresh_token

async def check_user_admin(token: str):
    try:
        user = await get_current_user(token)
        if user.is_superuser != True or user.is_active != True or user == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't have the access.")
        return True
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")