# main.py

import os
import pandas as pd
from datetime import datetime
from config import EXCEL_FILE_PATH, USER_SETTINGS_FILE_PATH
from utils import (
    read_excel_data,
    get_currency_rates,
    get_stock_prices,
    calculate_cashback,
    get_greeting,
    search_phone_numbers,
    read_transactions_from_xlsx
)

def test_read_excel_data():
    # Пример использования функции read_excel_data
    end_date = datetime.now().strftime('%Y-%m-%d')
    df = read_excel_data(EXCEL_FILE_PATH, end_date)
    print("Данные из Excel:")
    print(df.head())

def test_get_currency_rates():
    # Пример использования функции get_currency_rates
    currencies = ['USD', 'EUR', 'GBP']
    rates = get_currency_rates(currencies)
    print("Курсы валют:")
    print(rates)

def test_get_stock_prices():
    # Пример использования функции get_stock_prices
    stocks = ['AAPL', 'GOOGL', 'MSFT']
    prices = get_stock_prices(stocks)
    print("Цены на акции:")
    print(prices)

def test_calculate_cashback():
    # Пример использования функции calculate_cashback
    total_spent = 1000.0
    cashback = calculate_cashback(total_spent)
    print(f"Кэшбэк за ${total_spent}: ${cashback}")

def test_get_greeting():
    # Пример использования функции get_greeting
    now = datetime.now()
    greeting = get_greeting(now)
    print(f"Приветствие для {now}: {greeting}")

def test_search_phone_numbers():
    # Пример использования функции search_phone_numbers
    transactions = [
        {'description': 'Оплата услуг по номеру 123-456-7890'},
        {'description': 'Снятие наличных в банкомате'},
        {'description': 'Оплата Джону Доу'}
    ]
    transactions_with_phones = search_phone_numbers(transactions)
    print("Транзакции с номерами телефонов:")
    print(transactions_with_phones)

def test_read_transactions_from_xlsx():
    # Пример использования функции read_transactions_from_xlsx
    transactions = read_transactions_from_xlsx(USER_SETTINGS_FILE_PATH)
    print("Транзакции из XLSX:")
    print(transactions)

if __name__ == "__main__":
    test_read_excel_data()
    print()

    test_get_currency_rates()
    print()

    test_get_stock_prices()
    print()

    test_calculate_cashback()
    print()

    test_get_greeting()
    print()

    test_search_phone_numbers()
    print()

    test_read_transactions_from_xlsx()
    print()
