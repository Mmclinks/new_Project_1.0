import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Определение базового пути проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Получение API ключа из переменных окружения
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

# Конфигурация API
EXCHANGE_API_URL = 'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'
EXCHANGE_API_KEY = os.getenv('EXCHANGE_API_KEY')