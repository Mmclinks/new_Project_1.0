import pandas as pd
import pytest
from src.views import get_greeting, get_main_page_data


def test_get_greeting():
    assert get_greeting(pd.Timestamp('2023-07-19 06:00:00')) == "Доброе утро"
    assert get_greeting(pd.Timestamp('2023-07-19 13:00:00')) == "Добрый день"
    assert get_greeting(pd.Timestamp('2023-07-19 19:00:00')) == "Добрый вечер"
    assert get_greeting(pd.Timestamp('2023-07-19 23:00:00')) == "Доброй ночи"


def test_get_main_page_data():
    data = get_main_page_data('2023-07-19 14:30:00')
    assert "greeting" in data
    assert "cards" in data
    assert "currency_rates" in data
    assert "stock_prices" in data
