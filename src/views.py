import json
import logging
from typing import Dict, List, Any
import pandas as pd
import requests
from typing import List, Dict
from datetime import datetime
# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Константы
USER_SETTINGS_FILE = 'user_settings.json'
CURRENCY_API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'
STOCK_API_URL = 'https://api.example.com/stock_prices'  # Подставьте реальный URL


def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие на основе текущего времени."""
    if 5 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"



def load_user_settings() -> Dict[str, Any]:
    """Загружает пользовательские настройки из JSON-файла."""
    with open(USER_SETTINGS_FILE, 'r') as file:
        return json.load(file)


def get_currency_rates(api_url: str, currencies: List[str]) -> List[Dict[str, float]]:
    """
    Получает курсы валют из API.

    :param api_url: URL для получения курсов валют
    :param currencies: Список валют, для которых нужно получить курсы
    :return: Список словарей с курсами валют
    """
    response = requests.get(api_url)
    data = response.json()

    rates = [
        {"currency": currency, "rate": data["rates"].get(currency, None)}
        for currency in currencies
    ]

    return rates







import requests
from requests.exceptions import ConnectionError, RequestException

def get_stock_prices(api_url, stocks):
    try:
        response = requests.get(api_url, params={'symbol': stocks})
        response.raise_for_status()  # Вызовет ошибку для некорректных ответов
        return response.json()  # Предполагается, что ответ в формате JSON
    except ConnectionError as ce:
        print(f"Ошибка подключения к {api_url}: {ce}")
    except RequestException as re:
        print(f"Ошибка запроса: {re}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")

    return None  # Или обработать адекватно в вашем приложении

# Пример использования
api_url = 'https://www.alphavantage.co/query'
stocks = 'AAPL'  # Пример символа акции
data = get_stock_prices(api_url, stocks)
if data:
    print(data)
else:
    print("Не удалось получить цены на акции.")


def get_top_transactions(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """Возвращает топ-5 транзакций по сумме платежа."""
    top_transactions = transactions.nlargest(5, 'Сумма операции')
    return top_transactions.to_dict(orient='records')


def analyze_expenses(transactions: pd.DataFrame) -> Dict[str, Any]:
    """Анализирует расходы и кешбэк по каждой карте."""
    cards = transactions.groupby('Номер карты').agg({
        'Сумма операции': 'sum'
    }).reset_index()
    cards['last_digits'] = cards['Номер карты'].astype(str).str[-4:]
    cards['cashback'] = cards['Сумма операции'] / 100.0
    cards.rename(columns={'Сумма операции': 'total_spent'}, inplace=True)
    return cards.to_dict(orient='records')
