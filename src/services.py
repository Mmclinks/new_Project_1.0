import pandas as pd
import json
import re
import logging
from typing import List, Dict
import requests
from typing import Dict
from config import EXCHANGE_API_URL, EXCHANGE_API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def find_phone_numbers(transactions: pd.DataFrame) -> str:
    """
    Находит все транзакции, содержащие в описании мобильные номера.

    :param transactions: Датафрейм с транзакциями.
    :return: JSON-строка с транзакциями, содержащими мобильные номера.
    """
    try:
        # Регулярное выражение для поиска мобильных номеров
        phone_pattern = re.compile(r'\+7\s?\d{3}\s?\d{3}-?\d{2}-?\d{2}')

        # Функция для проверки наличия номера в описании
        contains_phone_number = lambda description: bool(phone_pattern.search(description))

        # Фильтруем транзакции, оставляем только те, у которых описание содержит номер
        filtered_transactions = transactions[transactions['Описание'].apply(contains_phone_number)]

        # Преобразуем в JSON
        result = filtered_transactions.to_dict(orient='records')
        json_result = json.dumps(result, ensure_ascii=False, indent=4)

        # Логируем информацию о выполнении
        logging.info("Поиск телефонных номеров завершен успешно.")

        return json_result

    except Exception as e:
        logging.error(f"Ошибка в функции find_phone_numbers: {e}")
        raise
