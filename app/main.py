import json

import sqlite3

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import CHATBOT_PATH, STATIC_DIR
from app.core.database import init_db
from app.routes.web import router as web_router
from chainlit.utils import mount_chainlit


sqlite3.register_adapter(dict, json.dumps)
sqlite3.register_adapter(list, json.dumps)

app = FastAPI(title="RAG App", version="1.0.0")


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


@app.get("/")
def read_main():
    return {"message": "Hello, World!"}


mount_chainlit(app=app, target=str(CHATBOT_PATH), path="/chatbot")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(web_router)
