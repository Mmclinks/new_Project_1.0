import pandas as pd
import pytest
from src.utils import load_data, format_datetime

def test_load_data():
    df = load_data('data/operations.xlsx')
    assert not df.empty

def test_format_datetime():
    dt_str = '2023-07-19 14:30:00'
    dt = format_datetime(dt_str)
    assert dt == pd.Timestamp('2023-07-19 14:30:00')
