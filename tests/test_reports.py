import unittest
import pytest
import pandas as pd
import json
from src.reports import spending_by_weekday  # Замените 'your_module' на имя вашего модуля


class TestSpendingByWeekday(unittest.TestCase):

    def setUp(self):
        # Создание тестовых данных
        self.data = {
            'Дата операции': pd.to_datetime(['2024-07-01', '2024-07-02', '2024-07-03', '2024-07-05', '2024-07-07']),
            'Сумма операции': [100, 200, 300, 400, 500]
        }
        self.df = pd.DataFrame(self.data)

    def test_no_matching_dates(self):
        date_str = '2024-06-30 18:00:00'
        expected_output = json.dumps([], ensure_ascii=False)

        result = spending_by_weekday(self.df, date_str)
        self.assertEqual(result, expected_output)

    def test_empty_dataframe(self):
        empty_df = pd.DataFrame(columns=['Дата операции', 'Сумма операции'])
        date_str = '2024-07-05 18:00:00'
        expected_output = json.dumps([], ensure_ascii=False)

        result = spending_by_weekday(empty_df, date_str)
        self.assertEqual(result, expected_output)


@pytest.fixture
def sample_df():
    data = {
        'Дата операции': [
            '2024-07-01 12:34:56',
            '2024-07-02 09:21:15',
            '2024-07-03 14:12:30',
            '2024-07-04 16:40:00'
        ],
        'Сумма операции': [100, 150, 200, 50]
    }
    return pd.DataFrame(data)


def test_spending_by_weekday_valid_data(sample_df):
    result = spending_by_weekday(sample_df, '2024-07-15 10:00:00')
    expected = [
        {"День недели": "Monday", "Сумма операции": 100},
        {"День недели": "Tuesday", "Сумма операции": 150},
        {"День недели": "Wednesday", "Сумма операции": 200},
        {"День недели": "Thursday", "Сумма операции": 50}
    ]
    assert json.loads(result) == expected


def test_spending_by_weekday_empty_df():
    empty_df = pd.DataFrame(columns=['Дата операции', 'Сумма операции'])
    result = spending_by_weekday(empty_df, '2024-07-15 10:00:00')
    assert json.loads(result) == []


def test_spending_by_weekday_invalid_date_format(sample_df):
    result = spending_by_weekday(sample_df, '2024-07-15')
    assert json.loads(result) == {"error": "Не удалось сгенерировать отчет"}


def test_spending_by_weekday_no_data_for_month(sample_df):
    result = spending_by_weekday(sample_df, '2024-08-15 10:00:00')
    assert json.loads(result) == []
