import json

import pytest
import pandas as pd
from datetime import datetime
from src.views import generate_json_response


def test_generate_json_response():
    # Пример данных
    data = {
        'Дата операции': ['2024-07-19', '2024-07-20', '2024-07-15'],
        'Номер карты': [1234567812345678, 8765432187654321, 1234567812345678],
        'Сумма операции': [1000, 2000, 1500],
        'Описание': ['Покупка 1', 'Покупка 2', 'Покупка 3']
    }
    df = pd.DataFrame(data)

    # Пример вызова функции
    response = generate_json_response('2024-07-20 12:00:00', df)

    # Проверка наличия ключей в ответе
    response_data = json.loads(response)
    assert "greeting" in response_data
    assert "cards" in response_data
    assert "top_transactions" in response_data
    assert "currency_rates" in response_data
    assert "stock_prices" in response_data

    # Дополнительные проверки можно добавить в зависимости от требуемых данных


if __name__ == '__main__':
    pytest.main()
