from fastapi import FastAPI

from app.auth.handlers import router as auth_router
from app.chats.handlers import router as chat_router
from app.friendship.handlers import router as friendship_router
from app.sockets.handlers import router as socket_router

app = FastAPI()

prefix_http = "/api/v1"
prefix_ws = "/ws"

app.include_router(auth_router, prefix=prefix_http)
app.include_router(friendship_router, prefix=prefix_http)
app.include_router(chat_router, prefix=prefix_http)
app.include_router(socket_router, prefix=prefix_ws)
