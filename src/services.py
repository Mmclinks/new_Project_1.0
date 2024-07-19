import pandas as pd
import json
import re
from typing import List, Dict, Any
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

def load_data(file_path: str) -> pd.DataFrame:
    """Загружает данные из Excel-файла."""
    return pd.read_excel(file_path)

def analyze_cashback_categories(data: pd.DataFrame, year: int, month: int) -> str:
    """Анализирует выгодность категорий повышенного кешбэка."""
    filtered_data = data[
        (pd.to_datetime(data['Дата операции']).dt.year == year) &
        (pd.to_datetime(data['Дата операции']).dt.month == month)
    ]

    category_cashback = (
        filtered_data.groupby('Категория')['Сумма операции']
        .apply(lambda x: (x // 100).sum())
        .to_dict()
    )

    logging.info(f"Категории кешбэка за {year}-{month}: {category_cashback}")

    return json.dumps(category_cashback, ensure_ascii=False)

def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Возвращает сумму, отложенную в инвесткопилку."""
    total_investment = 0

    for transaction in transactions:
        transaction_date = pd.to_datetime(transaction['Дата операции'])
        transaction_month = transaction_date.strftime('%Y-%m')

        if transaction_month == month:
            amount = transaction['Сумма операции']
            rounded_amount = (amount + limit - 1) // limit * limit
            total_investment += rounded_amount - amount

    logging.info(f"Общая сумма в инвесткопилке за {month}: {total_investment}")

    return total_investment

def simple_search(data: pd.DataFrame, query: str) -> str:
    """Возвращает все транзакции, содержащие запрос в описании или категории."""
    result = data[
        data['Описание'].str.contains(query, case=False, na=False) |
        data['Категория'].str.contains(query, case=False, na=False)
    ]

    transactions = result.to_dict(orient='records')
    logging.info(f"Найдено {len(transactions)} транзакций по запросу '{query}'")

    return json.dumps(transactions, ensure_ascii=False)

def search_phone_numbers(data: pd.DataFrame) -> str:
    """Возвращает все транзакции, содержащие в описании мобильные номера."""
    phone_pattern = re.compile(r'\+7 \d{3} \d{2}-\d{2}-\d{2}')
    result = data[data['Описание'].str.contains(phone_pattern, na=False)]

    transactions = result.to_dict(orient='records')
    logging.info(f"Найдено {len(transactions)} транзакций с телефонными номерами")

    return json.dumps(transactions, ensure_ascii=False)

def search_personal_transfers(data: pd.DataFrame) -> str:
    """Возвращает все транзакции, относящиеся к переводам физлицам."""
    transfer_pattern = re.compile(r'\b[А-Я][а-я]+\s[А-Я]\.\b')
    result = data[
        (data['Категория'] == 'Переводы') &
        data['Описание'].str.contains(transfer_pattern, na=False)
    ]

    transactions = result.to_dict(orient='records')
    logging.info(f"Найдено {len(transactions)} переводов физлицам")

    return json.dumps(transactions, ensure_ascii=False)
