from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.database import init_db

from server.routes.auth_apis import router as AuthRouter
from server.routes.post_apis import router as PostRouter
from server.routes.user_apis import router as UserRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter, tags=["User APIs"], prefix="/users")
app.include_router(AuthRouter, tags=["Authentication APIs"], prefix="/auth")
app.include_router(PostRouter, tags=["Post APIs"], prefix="/posts")

app = FastAPI()

@app.on_event("startup")
async def start_db():
    await init_db()
    
@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Welcome to your beanie powered app!"}