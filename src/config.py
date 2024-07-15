import os
from dotenv import load_dotenv

load_dotenv()

EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH")
USER_SETTINGS_FILE_PATH = os.getenv("USER_SETTINGS_FILE_PATH")
CURRENCY_API_URL = os.getenv("CURRENCY_API_URL")
STOCK_API_URL = os.getenv("STOCK_API_URL")
