import sqlite3
import json
from fastapi import FastAPI
from core.database import init_db
from chainlit.utils import mount_chainlit


sqlite3.register_adapter(dict, json.dumps)
sqlite3.register_adapter(list, json.dumps)
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
def read_main():
    return {"message": "Hello, World!"}

mount_chainlit(app=app, target="chatbot.py", path="/chatbot")