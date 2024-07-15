import os
import unittest
from datetime import datetime

import pandas as pd

from src.utils import read_excel_data, search_phone_numbers


class TestMyFunctions(unittest.TestCase):

    def setUp(self):
        # Мокаем данные для тестирования
        self.test_data = [
            {"date": "2024-06-15", "value": 100},
            {"date": "2024-06-25", "value": 200},
            {"date": "2024-07-05", "value": 300}
        ]

    def test_read_excel_data(self):
        # Создаем временный файл Excel
        file_path = "test_data.xlsx"
        df = pd.DataFrame(self.test_data)
        df.to_excel(file_path, index=False)

        # Тестируем функцию read_excel_data
        end_date = datetime(2024, 6, 30)
        result_df = read_excel_data(file_path, end_date)

        # Проверяем, что данные фильтруются корректно
        self.assertEqual(len(result_df), 2)  # Ожидаем две строки в результате

    def test_search_phone_numbers(self):
        # Тестируем функцию search_phone_numbers
        transactions = [
            {"description": "Payment for phone bill 123-456-7890"},
            {"description": "Purchase at store"},
            {"description": "Received payment from 555.123.4567"}
        ]

        result = search_phone_numbers(transactions)

        # Проверяем, что функция правильно находит номера телефонов
        self.assertEqual(len(result), 2)  # Ожидаем две транзакции с номерами телефонов

        # Проверяем конкретные ожидаемые результаты
        self.assertIn(transactions[0], result)
        self.assertIn(transactions[2], result)

    def tearDown(self):
        # Удаление временного файла Excel после тестов
        try:
            os.remove("test_data.xlsx")
        except FileNotFoundError:
            pass
