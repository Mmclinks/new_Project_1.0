import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import pandas as pd

from src.views import generate_homepage_data
from src.views import spending_by_weekday
from src.utils import read_excel_data, get_currency_rates, get_stock_prices, search_phone_numbers


class TestGenerateHomepageData(unittest.TestCase):

    @patch('src.utils.read_excel_data')
    @patch('src.utils.get_currency_rates')
    @patch('src.utils.get_stock_prices')
    @patch('src.utils.search_phone_numbers')
    @patch('os.getenv')
    def test_generate_homepage_data(self, mock_getenv, mock_search_phone_numbers, mock_get_stock_prices,
                                    mock_get_currency_rates, mock_read_excel_data):
        # Установка моков
        mock_getenv.return_value = 'test_file.xlsx'

        mock_transactions = [
            {"Date": datetime(2024, 6, 15), "Amount": 100, "Description": "Test transaction 1"},
            {"Date": datetime(2024, 6, 20), "Amount": 150, "Description": "Test transaction 2"},
            {"Date": datetime(2024, 6, 25), "Amount": 200, "Description": "Test transaction 3"},
        ]

        mock_read_excel_data.return_value = mock_transactions
        mock_currency_rates = [{"currency": "USD", "rate": 70.0}, {"currency": "EUR", "rate": 80.0}]
        mock_get_currency_rates.return_value = mock_currency_rates
        mock_stock_prices = [{"stock": "AAPL", "price": 150.0}, {"stock": "GOOG", "price": 2000.0}]
        mock_get_stock_prices.return_value = mock_stock_prices
        mock_transactions_with_phones = [mock_transactions[0], mock_transactions[2]]
        mock_search_phone_numbers.return_value = mock_transactions_with_phones

        # Вызов функции с тестовыми данными
        result = generate_homepage_data('2024-07-01')

        # Проверки результата
        self.assertEqual(result["greeting"], "Hello, user!")
        self.assertEqual(result["currency_rates"], mock_currency_rates)
        self.assertEqual(result["stock_prices"], mock_stock_prices)
        self.assertEqual(result["cards"], mock_transactions)
        self.assertEqual(result["top_transactions"], mock_transactions[:5])
        self.assertEqual(result["transactions_with_phones"], mock_transactions_with_phones)

        # Проверка вызовов функций
        mock_getenv.assert_called_once_with('EXCEL_FILE_PATH')
        mock_read_excel_data.assert_called_once_with('test_file.xlsx', '2024-07-01')
        mock_get_currency_rates.assert_called_once()
        mock_get_stock_prices.assert_called_once()
        mock_search_phone_numbers.assert_called_once_with(mock_transactions)


class TestSpendingByWeekday(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые данные для каждого дня недели за последние три месяца
        today = datetime.now().date()
        self.test_data = [
            {"Date": today - timedelta(days=10), "Amount": 100},
            {"Date": today - timedelta(days=15), "Amount": 150},
            {"Date": today - timedelta(days=20), "Amount": 200},
            {"Date": today - timedelta(days=25), "Amount": 250},
            {"Date": today - timedelta(days=30), "Amount": 300},
            {"Date": today - timedelta(days=35), "Amount": 350},
            {"Date": today - timedelta(days=40), "Amount": 400}
        ]
        self.test_df = pd.DataFrame(self.test_data)

    def test_spending_by_weekday(self):
        # Тестирование функции spending_by_weekday

        # Вызываем функцию с тестовыми данными
        result_df = spending_by_weekday(self.test_df)

        # Проверяем, что результат содержит все дни недели
        expected_weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.assertEqual(list(result_df['Weekday']), expected_weekdays)

        # Проверяем, что для каждого дня недели считается среднее значение трат
        expected_averages = [350, 300, 250, 200, 150, 100, 0]  # Последний день - это текущий день теста, так что 0
        for i, avg in enumerate(expected_averages):
            self.assertAlmostEqual(result_df.loc[i, 'Average Spending'], avg, delta=0.01)

    def tearDown(self):
        # Очистка после выполнения теста
        pass
