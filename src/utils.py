# utils.py

import requests
import re
import pandas as pd
import openpyxl
from datetime import datetime
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_excel_data(file_path: str, end_date: str) -> pd.DataFrame:
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    start_date = end_date.replace(day=1)

    try:
        df = pd.read_excel(file_path)
        df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' column is present and in correct format
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        return filtered_df
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return pd.DataFrame()

def get_currency_rates(currencies: List[str]) -> List[Dict[str, float]]:
    rates = []
    for currency in currencies:
        try:
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{currency}")
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            rates.append({"currency": currency, "rate": data["rates"]["RUB"]})
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе курса валюты {currency}: {e}")
    return rates

def get_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    prices = []
    for stock in stocks:
        try:
            response = requests.get(f"https://api.your-real-stock-api.com/stock/{stock}")
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            prices.append({"stock": stock, "price": data["price"]})
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе цены акции {stock}: {e}")
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

def search_phone_numbers(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    phone_number_pattern = r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"
    transactions_with_phones = []

    for transaction in transactions:
        description = transaction.get('description', '')
        if re.search(phone_number_pattern, description):
            transactions_with_phones.append(transaction)

    return transactions_with_phones

def read_transactions_from_xlsx(xlsx_file: str) -> List[Dict[str, Any]]:
    transactions: List[Dict[str, Any]] = []

    try:
        workbook = openpyxl.load_workbook(xlsx_file)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]

        for row in sheet.iter_rows(min_row=2, values_only=True):
            transaction = dict(zip(headers, row))

            if 'дата операции' in transaction and isinstance(transaction['дата операции'], datetime):
                transaction['дата операции'] = transaction['дата операции'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')

            if 'сумма операции' in transaction:
                try:
                    transaction['сумма операции'] = float(transaction['сумма операции'])
                except (TypeError, ValueError):
                    pass

            transactions.append(transaction)

        logger.info(f"Успешно прочитан XLSX-файл: {xlsx_file}")
    except FileNotFoundError:
        logger.error(f"Файл не найден: {xlsx_file}")
    except Exception as e:
        logger.error(f"Ошибка при чтении XLSX-файла {xlsx_file}: {e}")

    return transactions
