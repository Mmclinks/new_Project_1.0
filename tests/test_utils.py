import logging
import os
import unittest
from datetime import datetime
from unittest.mock import patch

import pandas as pd

from src.utils import get_greeting, read_transactions_from_excel


class TestGetGreeting(unittest.TestCase):

    def test_morning_greeting(self):
        # Время с 5:00 до 11:59
        self.assertEqual(get_greeting(datetime(2024, 7, 20, 5, 0, 0)), "Доброе утро")
        self.assertEqual(get_greeting(datetime(2024, 7, 20, 11, 59, 59)), "Доброе утро")

    def test_afternoon_greeting(self):
        # Время с 12:00 до 17:59
        self.assertEqual(get_greeting(datetime(2024, 7, 20, 12, 0, 0)), "Добрый день")
        self.assertEqual(get_greeting(datetime(2024, 7, 20, 17, 59, 59)), "Добрый день")

    def test_evening_greeting(self):
        # Время с 18:00 до 22:59
        self.assertEqual(get_greeting(datetime(2024, 7, 20, 18, 0, 0)), "Добрый вечер")
        self.assertEqual(get_greeting(datetime(2024, 7, 20, 22, 59, 59)), "Добрый вечер")

    def test_night_greeting(self):
        # Время с 23:00 до 4:59
        self.assertEqual(get_greeting(datetime(2024, 7, 20, 23, 0, 0)), "Доброй ночи")
        self.assertEqual(get_greeting(datetime(2024, 7, 20, 4, 59, 59)), "Доброй ночи")


if __name__ == '__main__':
    unittest.main()


class TestReadTransactionsFromExcel(unittest.TestCase):

    def setUp(self):
        # Создание тестового Excel файла
        self.file_path = 'test_transactions.xlsx'
        data = {
            'Дата операции': ['2024-07-01', '2024-07-02'],
            'Описание': ['Оплата по телефону +1234567890', 'Оплата по телефону +0987654321'],
            'Сумма операции': [100, 200]
        }
        self.df = pd.DataFrame(data)
        self.df.to_excel(self.file_path, index=False)

    def tearDown(self):
        # Удаление тестового файла после тестов
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_read_valid_excel_file(self):
        result = read_transactions_from_excel(self.file_path)
        from pandas._testing import assert_frame_equal
        assert_frame_equal(result, self.df)

    def test_file_not_found(self):
        result = read_transactions_from_excel('non_existent_file.xlsx')
        self.assertIsNone(result)

    @patch('pandas.read_excel', side_effect=Exception('Mocked exception'))
    def test_read_excel_exception(self, mock_read_excel):
        result = read_transactions_from_excel(self.file_path)
        self.assertIsNone(result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    unittest.main()
