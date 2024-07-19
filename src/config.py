import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

EXCEL_FILE_PATH = BASE_DIR / "operations.xlsx"
USER_SETTINGS_FILE_PATH = BASE_DIR / "user_settings.json"
API_LAYER_ACCESS_KEY = os.getenv("API_LAYER_ACCESS_KEY")
NASDAQ_API_KEY = os.getenv("NASDAQ_API_KEY")