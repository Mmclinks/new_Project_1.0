from src.views import spending_by_weekday  # замените 'your_module' на имя вашего модуля
import pytest
from unittest.mock import patch, MagicMock
from src.views import generate_homepage_data  # замените 'your_module' на имя вашего модуля
import pandas as pd

sample_data = {
    'Date': pd.date_range(start='2023-01-01', periods=100),
    'Amount': [100, 200, 150, 300, 250, 180, 220, 210, 190, 280] * 10  # повторяем для большего набора данных
}
transactions_df = pd.DataFrame(sample_data)


def test_spending_by_weekday_no_transactions():
    # Проверка поведения при отсутствии транзакций в указанном диапазоне
    empty_df = pd.DataFrame(columns=['Date', 'Amount'])
    result_df = spending_by_weekday(empty_df, date='2023-04-01')
    assert result_df.empty  # ожидаем пустой DataFrame


def test_spending_by_weekday_missing_columns():
    # Проверка обработки ошибки при отсутствии ожидаемых столбцов в DataFrame
    invalid_df = pd.DataFrame({'Datum': pd.date_range(start='2023-01-01', periods=100), 'Amount': [100] * 100})
    result_df = spending_by_weekday(invalid_df, date='2023-04-01')
    assert result_df.empty  # ожидаем пустой DataFrame





# Пример данных для тестирования
sample_transactions = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=100),
    'Amount': [100, 200, 150, 300, 250, 180, 220, 210, 190, 280] * 10  # повторяем для большего набора данных
})

sample_currency_rates = {
    'USD': 74.0,
    'EUR': 88.0
}

sample_stock_prices = {
    'AAPL': 150.0,
    'GOOGL': 2800.0
}

sample_transactions_with_phones = sample_transactions.copy()
sample_transactions_with_phones['Phone'] = ['1234567890'] * len(sample_transactions_with_phones)

EXCEL_FILE_PATH = 'path/to/your/excel/file.xlsx'
