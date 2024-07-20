import json
import unittest
from unittest.mock import mock_open, patch

import pytest
import requests
from flask import Flask

from src.views import get_currency_rates, get_stock_prices, main_page_analysis


@pytest.fixture
def app():
    app = Flask(__name__)
    app.add_url_rule('/main', 'main_page_analysis', main_page_analysis, methods=['GET'])
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestGetStockPrices(unittest.TestCase):

    @patch('src.views.requests.get')  # Убедитесь, что путь правильный
    @patch('src.views.open', new_callable=mock_open, read_data='{"user_stocks": ["AAPL", "GOOGL"]}')
    def test_get_stock_prices_success(self, mock_open, mock_get):
        # Mock the API responses
        mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: {'c': 150.0}),
            unittest.mock.Mock(json=lambda: {'c': 2800.0}),
        ]

        expected_output = [
            {"stock": "AAPL", "price": 150.0},
            {"stock": "GOOGL", "price": 2800.0}
        ]

        result = get_stock_prices()
        self.assertEqual(result, expected_output)

    @patch('src.views.requests.get')
    @patch('src.views.open', new_callable=mock_open, read_data='{"user_stocks": []}')
    def test_get_stock_prices_no_stocks(self, mock_open, mock_get):
        # Mock the API responses
        mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: {'c': 150.0}),
            unittest.mock.Mock(json=lambda: {'c': 2800.0}),
        ]

        expected_output = []  # No stocks to fetch

        result = get_stock_prices()
        self.assertEqual(result, expected_output)

    @patch('src.views.requests.get')
    @patch('src.views.open', new_callable=mock_open, read_data='{"user_stocks": ["AAPL", "GOOGL"]}')
    def test_get_stock_prices_api_error(self, mock_open, mock_get):
        # Mock an API response with an error
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        with self.assertRaises(requests.exceptions.RequestException):
            get_stock_prices()

    @patch('src.views.requests.get')
    @patch('src.views.open', new_callable=mock_open)
    def test_get_stock_prices_file_error(self, mock_open, mock_get):
        # Mock a file read error
        mock_open.side_effect = IOError("File not found")

        with self.assertRaises(IOError):
            get_stock_prices()


class TestGetCurrencyRates(unittest.TestCase):

    @patch('src.views.requests.get')
    @patch('src.views.open', new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
    def test_get_currency_rates_success(self, mock_open, mock_get):
        # Подготовка данных для теста
        api_key = "test_api_key"
        mock_response = {
            'rates': {
                'USD': 74.0,
                'EUR': 88.0
            }
        }
        mock_get.return_value.json.return_value = mock_response

        expected_output = json.dumps([
            {"currency": "USD", "rate": 74.0},
            {"currency": "EUR", "rate": 88.0}
        ], ensure_ascii=False)

        # Вызов тестируемой функции
        result = get_currency_rates(api_key)

        # Проверка результата
        self.assertEqual(result, expected_output)
        mock_get.assert_called_once_with(f"https://api.exchangerate-api.com/v4/latest/RUB?apikey={api_key}")
        mock_open.assert_called_once_with("src/user_settings.json", "r")

    @patch('src.views.requests.get')
    @patch('src.views.open', new_callable=mock_open, read_data='{}')
    def test_get_currency_rates_no_currencies(self, mock_open, mock_get):
        # Подготовка данных для теста
        api_key = "test_api_key"
        mock_response = {
            'rates': {
                'USD': 74.0,
                'EUR': 88.0
            }
        }
        mock_get.return_value.json.return_value = mock_response

        expected_output = json.dumps([], ensure_ascii=False)

        # Вызов тестируемой функции
        result = get_currency_rates(api_key)

        # Проверка результата
        self.assertEqual(result, expected_output)
        mock_get.assert_called_once_with(f"https://api.exchangerate-api.com/v4/latest/RUB?apikey={api_key}")
        mock_open.assert_called_once_with("src/user_settings.json", "r")


if __name__ == '__main__':
    unittest.main()
