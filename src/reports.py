import pandas as pd
import json
import logging
from datetime import datetime
from typing import Optional, Callable, Dict
import functools

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def report_to_file(filename: Optional[str] = None):
    """
    Декоратор для записи результата функции в файл.
    Если имя файла не задано, используется имя по умолчанию.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Использование имени файла по умолчанию, если не задано
            if filename is None:
                filename = f"{func.__name__}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as file:
                json.dump(result, file, indent=4)
            logging.info(f"Report saved to {filename}")
            return result
        return wrapper
    return decorator


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    end_date = pd.Timestamp(date)
    start_date = end_date - pd.DateOffset(months=3)

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    filtered_data = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date) &
        (transactions['Категория'] == category)
        ]

    total_spent = filtered_data['Сумма операции'].sum()
    return {"Категория": category, "Траты за последние три месяца": total_spent}


@report_to_file()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    end_date = pd.Timestamp(date)
    start_date = end_date - pd.DateOffset(months=3)

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    filtered_data = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date)
        ]

    filtered_data['День недели'] = filtered_data['Дата операции'].dt.day_name()
    weekday_spending = filtered_data.groupby('День недели')['Сумма операции'].mean().to_dict()

    return {"Средние траты по дням недели": weekday_spending}


@report_to_file()
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает средние траты в рабочий и выходной день за последние три месяца (от переданной даты)."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    end_date = pd.Timestamp(date)
    start_date = end_date - pd.DateOffset(months=3)

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    filtered_data = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date)
        ]

    filtered_data['Рабочий день'] = filtered_data['Дата операции'].dt.weekday < 5
    workday_spending = filtered_data.groupby('Рабочий день')['Сумма операции'].mean().to_dict()

    return {
        "Средние траты в рабочие дни": workday_spending.get(True, 0),
        "Средние траты в выходные дни": workday_spending.get(False, 0)
    }
