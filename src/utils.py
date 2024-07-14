import pandas as pd
import requests
import datetime
import logging
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)


def read_excel_data(file_path: str, end_date: datetime) -> pd.DataFrame:
    # Преобразовать строку end_date в объект datetime
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    start_date = end_date.replace(day=1)
    df = pd.read_excel(file_path)
    df['date'] = pd.to_datetime(df['date'])
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return df


def get_currency_rates(currencies: list) -> list:
    rates = []
    for currency in currencies:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{currency}")
        data = response.json()
        rates.append({"currency": currency, "rate": data["rates"]["RUB"]})
    return rates


def get_stock_prices(stocks: list) -> list:
    prices = []
    for stock in stocks:
        response = requests.get(f"https://api.example.com/stock/{stock}")
        data = response.json()
        prices.append({"stock": stock, "price": data["price"]})
    return prices


def calculate_cashback(total_spent: float) -> float:
    return total_spent * 0.01


def get_greeting(date: datetime) -> str:
    hour = date.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def search_phone_numbers(transactions):
    """
    Search for phone numbers in transaction descriptions.

    Args:
    - transactions (list): List of dictionaries representing transactions.

    Returns:
    - list: List of transactions containing phone numbers in the description.
    """
    phone_number_pattern = r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"
    transactions_with_phones = []

    for transaction in transactions:
        description = transaction.get('description', '')
        if re.search(phone_number_pattern, description):
            transactions_with_phones.append(transaction)

    return transactions_with_phones
