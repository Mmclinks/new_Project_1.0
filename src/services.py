import json
import logging
import re
from typing import Any, Dict, List


def search_by_phone(transactions: List[Dict[str, Any]], phone_number: str) -> str:
    """
    Ищет транзакции по номеру телефона в списке транзакций.

    Параметры:
    transactions (List[Dict[str, Any]]): Список словарей, представляющих транзакции.
    Каждый словарь должен содержать ключ 'Описание',
                                         в котором может находиться информация о номере телефона.
    phone_number (str): Номер телефона или регулярное выражение для поиска в поле 'Описание' транзакций.

    Возвращает:
    str: JSON строка, содержащая список транзакций, в которых найдено совпадение с номером телефона.
     Если возникла ошибка,
         возвращается JSON строка с сообщением об ошибке.
    """
    try:
        # Создание регулярного выражения для поиска номера телефона
        phone_pattern = re.compile(phone_number)

        # Поиск транзакций, содержащих совпадение с номером телефона
        matching_transactions = [txn for txn in transactions if phone_pattern.search(txn.get("Описание", ""))]

        # Преобразование результата в JSON строку
        return json.dumps(matching_transactions, ensure_ascii=False)
    except Exception as e:
        # Логирование ошибки и возврат сообщения об ошибке
        logging.error(f"Ошибка поиска по номеру телефона: {e}")
        return json.dumps({"error": "Не удалось выполнить поиск транзакций"})
