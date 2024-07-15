import pytest
import pandas as pd
from datetime import datetime

@pytest.fixture
def sample_transactions():
    data = {
        'card_number': [1234, 5678, 1234, 5678, 1234],
        'date': [
            datetime(2024, 7, 1),
            datetime(2024, 7, 5),
            datetime(2024, 7, 10),
            datetime(2024, 7, 15),
            datetime(2024, 7, 20)
        ],
        'amount': [100, 200, 300, 400, 500]
    }
    return pd.DataFrame(data)
