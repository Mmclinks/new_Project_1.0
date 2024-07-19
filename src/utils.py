import pandas as pd
import json
import datetime
from typing import Optional
from datetime import datetime
from datetime import datetime

def get_greeting(current_time: datetime) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    :param current_time: Текущее время
    :return: Приветствие
    """
    if 5 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_transactions(file_path):
    df = pd.read_excel(file_path)
    return df





def get_transactions_in_date_range(df: pd.DataFrame, input_date: str) -> pd.DataFrame:
    """
    Фильтрует транзакции по дате. Возвращает транзакции за последний месяц от переданной даты.

    :param df: DataFrame с транзакциями
    :param input_date: Входная дата в формате 'YYYY-MM-DD HH:MM:SS'
    :return: Отфильтрованный DataFrame
    """
    try:
        # Преобразование входной даты в формат datetime
        input_date_dt = pd.to_datetime(input_date, format='%Y-%m-%d %H:%M:%S')

        # Преобразование столбца 'Дата операции' в формат datetime с учетом формата
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')

        # Определение диапазона дат
        end_date = input_date_dt
        start_date = end_date - pd.DateOffset(months=3)

        # Фильтрация данных
        filtered_df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)]
        return filtered_df

    except Exception as e:
        print(f"Error in get_transactions_in_date_range: {e}")
        return pd.DataFrame()


def calculate_cashback(df):
    df['Cashback'] = df['Сумма операции'] / 100
    cashback_by_card = df.groupby('Последние 4 цифры карты')['Cashback'].sum().reset_index()
    total_spent_by_card = df.groupby('Последние 4 цифры карты')['Сумма операции'].sum().reset_index()

    results = []
    for _, row in total_spent_by_card.iterrows():
        cashback = cashback_by_card[cashback_by_card['Последние 4 цифры карты'] == row['Последние 4 цифры карты']][
            'Cashback'].sum()
        results.append({
            'last_digits': row['Последние 4 цифры карты'],
            'total_spent': row['Сумма операции'],
            'cashback': cashback
        })
    return results


def get_top_transactions(df, top_n=5):
    return df.nlargest(top_n, 'Сумма операции')[['Дата операции', 'Сумма операции', 'Категория', 'Описание']].to_dict(
        orient='records')


def get_greeting():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


# src/utils.py

import json
from typing import Dict, List, Optional

def load_user_settings(file_path: str) -> Dict[str, List[str]]:
    """
    Загружает настройки пользователя из JSON-файла.

    :param file_path: Путь к JSON-файлу
    :return: Словарь с настройками пользователя
    """
    with open(file_path, 'r') as f:
        settings = json.load(f)
    return settings
