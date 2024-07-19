import pandas as pd
from typing import List, Dict, Any


def load_data(file_path: str) -> pd.DataFrame:
    """Загружает данные из Excel-файла."""
    return pd.read_excel(file_path)


def format_datetime(datetime_str: str) -> pd.Timestamp:
    """Форматирует строку даты и времени в объект Timestamp."""
    return pd.to_datetime(datetime_str)


def get_expenses_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Возвращает суммарные расходы по каждой карте."""
    data['Кэшбэк'] = data['Сумма операции'] // 100  # 1 рубль на каждые 100 рублей
    summary = data.groupby('Номер карты').agg(
        {'Сумма операции': 'sum', 'Кэшбэк': 'sum'}
    ).reset_index()
    return summary


def get_income_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Возвращает суммарные доходы по каждой карте."""
    # Пример функции, возвращающей суммарные доходы (если такая информация присутствует в данных)
    summary = data.groupby('Номер карты').agg(
        {'Сумма платежа': 'sum'}
    ).reset_index()
    return summary


# Добавление дополнительных функций для анализа данных

def get_events_data(data: pd.DataFrame, date: pd.Timestamp, range: str) -> pd.DataFrame:
    """Функция для получения данных событий за определенный период."""
    if range == 'M':
        start_date = date - pd.DateOffset(months=1)
    elif range == 'W':
        start_date = date - pd.DateOffset(weeks=1)
    elif range == 'D':
        start_date = date - pd.DateOffset(days=1)
    else:
        raise ValueError("Неверный диапазон. Используйте 'M', 'W' или 'D'.")

    filtered_data = data[(data['Дата операции'] >= start_date) & (data['Дата операции'] <= date)]
    return filtered_data
