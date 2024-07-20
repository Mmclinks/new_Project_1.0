import logging
from datetime import datetime
from typing import Optional

import pandas as pd


def get_greeting(current_time: datetime) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    Параметры:
    current_time (datetime): Объект datetime, содержащий текущее время.

    Возвращает:
    str: Приветствие в зависимости от времени суток.
    Возможные значения: "Доброе утро", "Добрый день",
     "Добрый вечер", "Доброй ночи".
    """
    hour = current_time.hour

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def read_transactions_from_excel(file_path: str) -> Optional[pd.DataFrame]:
    """
    Читает данные транзакций из Excel файла.

    Параметры:
    file_path (str): Путь к Excel файлу, содержащему данные транзакций.

    Возвращает:
    pandas.DataFrame: Датафрейм с данными транзакций, если файл успешно прочитан.
    None: Если возникла ошибка при чтении файла.
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        logging.error(f"Ошибка при чтении Excel файла: {e}")
        return None


def calculate_cashback(total_spent: float) -> float:
    """
    Рассчитывает сумму кэшбэка на основе общей потраченной суммы.

    Параметры:
    total_spent (float): Общая сумма расходов.

    Возвращает:
    float: Сумма кэшбэка, рассчитанная как 1% от общей потраченной суммы.
    """
    return total_spent * 0.01
