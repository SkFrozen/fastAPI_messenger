from fastapi import FastAPI

from app.auth.handlers import router as auth_router
from app.chats.handlers import router as chat_router
from app.friendship.handlers import router as friendship_router

app = FastAPI()

prefix = "/api/v1"

app.include_router(auth_router, prefix=prefix)
app.include_router(friendship_router, prefix=prefix)
app.include_router(chat_router, prefix=prefix)
