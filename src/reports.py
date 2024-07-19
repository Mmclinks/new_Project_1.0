import pandas as pd
import datetime
import logging
from typing import Optional

import pandas as pd
from datetime import datetime
from typing import Dict, List
import requests
from config import ALPHA_VANTAGE_API_KEY
from pandas import read_excel
from src.views import get_stock_prices

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Вычисляет средние траты по дням недели за последние три месяца от переданной даты.

    :param transactions: Датафрейм с транзакциями.
    :param date: Опциональная дата в формате 'YYYY-MM-DD'. Если не указана, используется текущая дата.
    :return: Датафрейм с средними тратами по дням недели.
    """
    try:
        # Если дата не указана, берем текущую
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')

        # Преобразуем строку даты в объект datetime
        end_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        start_date = end_date - pd.DateOffset(months=3)

        # Преобразуем колонку с датами в формат datetime
        transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])

        # Фильтруем данные за последние три месяца
        filtered_transactions = transactions[(transactions['Дата операции'] >= start_date) &
                                             (transactions['Дата операции'] <= end_date)]

        # Добавляем колонку с днем недели
        filtered_transactions['Weekday'] = filtered_transactions['Дата операции'].dt.day_name()

        # Рассчитываем средние траты по дням недели
        spending_by_weekday = (filtered_transactions.groupby('Weekday')['Сумма операции']
                               .mean().reset_index())
        spending_by_weekday = spending_by_weekday.rename(columns={'Сумма операции': 'Средние траты'})

        # Логируем информацию о вычисленных данных
        logging.info("Расчет средних трат по дням недели завершен успешно.")

        return spending_by_weekday

    except Exception as e:
        logging.error(f"Ошибка в функции spending_by_weekday: {e}")
        raise


def create_excel_report(data: pd.DataFrame, output_file_path: str):
    """
    Создает Excel-отчет из DataFrame.

    :param data: DataFrame с данными для отчета.
    :param output_file_path: Путь к выходному Excel-файлу.
    """
    data.to_excel(output_file_path, index=False)



    def get_stock_prices(symbol: str) -> Dict[str, any]:
        """
        Получает цены акций из Alpha Vantage API.

        :param symbol: Символ акции.
        :return: Данные о ценах акций.
        """
        STOCK_API_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={ALPHA_VANTAGE_API_KEY}'
        response = requests.get(STOCK_API_URL)
        return response.json()

    def generate_json_response(file_path: str, date_time: str) -> Dict[str, any]:
        """
        Генерирует JSON-ответ на основе данных из Excel-файла и текущего времени.

        :param file_path: Путь к Excel-файлу.
        :param date_time: Дата и время в формате 'YYYY-MM-DD HH:MM:SS'.
        :return: JSON-ответ с данными о расходах, валютных курсах и ценах акций.
        """
        # Загрузка данных из Excel
        df = read_excel(file_path)

        # Приветствие
        now = datetime.now()
        hour = now.hour
        if 5 <= hour < 12:
            greeting = "Доброе утро"
        elif 12 <= hour < 18:
            greeting = "Добрый день"
        elif 18 <= hour < 23:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"

        # Получение данных о ценах акций
        symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        stock_prices = []
        for symbol in symbols:
            data = get_stock_prices(symbol)
            latest_price = data.get('Time Series (1min)', {}).popitem()[1].get('1. open', 'N/A')
            stock_prices.append({
                "stock": symbol,
                "price": float(latest_price)
            })

        # Пример данных для JSON-ответа (заполните данные в соответствии с вашей логикой)
        response_json = {
            "greeting": greeting,
            "cards": [
                {
                    "last_digits": "5814",
                    "total_spent": 1262.00,
                    "cashback": 12.62
                }
            ],
            "top_transactions": [
                {
                    "date": "21.12.2021",
                    "amount": 1198.23,
                    "category": "Переводы",
                    "description": "Перевод Кредитная карта. ТП 10.2 RUR"
                }
            ],
            "currency_rates": [
                {
                    "currency": "USD",
                    "rate": 73.21
                }
            ],
            "stock_prices": stock_prices
        }

        return response_json
