import os
from dotenv import load_dotenv
from src.utils import read_excel_data, get_currency_rates, get_stock_prices, search_phone_numbers, get_greeting
from typing import Optional
import pandas as pd
from datetime import timedelta, datetime
import logging

# Инициализация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    filtered_transactions = transactions.copy()
    filtered_transactions['Date'] = pd.to_datetime(filtered_transactions['Date'])

    # Проверка переданной даты или использование текущей даты
    if date is None:
        date = datetime.now().date()
    else:
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError as e:
            logger.error(f"Invalid date format: {date}. Error: {str(e)}")
            return pd.DataFrame()

    # Определяем дату начала - три месяца назад от указанной даты
    three_months_ago = date - timedelta(days=90)

    # Фильтруем транзакции за последние три месяца
    filtered_transactions = filtered_transactions[(filtered_transactions['Date'] >= three_months_ago) &
                                                  (filtered_transactions['Date'] <= date)]

    # Добавляем столбец с днем недели
    filtered_transactions['Weekday'] = filtered_transactions['Date'].dt.weekday

    # Группируем по дню недели и вычисляем средние траты
    average_spending = filtered_transactions.groupby('Weekday')['Amount'].mean()

    # Создаем DataFrame с результатами
    result_df = pd.DataFrame({
        'Weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'Average Spending': average_spending
    })

    return result_df


def generate_homepage_data(date: str) -> dict:
    try:
        file_path = os.getenv('EXCEL_FILE_PATH')
        transactions = read_excel_data(file_path, date)
        currency_rates = get_currency_rates(['USD', 'EUR', 'GBP'])  # Пример валют для получения курсов
        stock_prices = get_stock_prices(['AAPL', 'GOOGL', 'AMZN'])  # Пример акций для получения цен
        transactions_with_phones = search_phone_numbers(transactions)

        homepage_data = {
            "greeting": get_greeting(datetime.now()),
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
            "cards": transactions.to_dict(orient='records'),
            "top_transactions": transactions.head(5).to_dict(orient='records'),
            "transactions_with_phones": transactions_with_phones
        }

        return homepage_data

    except Exception as e:
        logger.error(f"Error generating homepage data: {str(e)}")
        return {}
