import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

BOT_TOKEN = os.environ.get('BOT_TOKEN')

STATES = {
    "GAME_SEARCH": "game_search"
}

URL_API = "http://localhost:8000/api/v1/"