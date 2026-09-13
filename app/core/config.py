import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = PROJECT_ROOT / "app"
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db")
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"
CHATBOT_PATH = APP_DIR / "chatbot.py"
