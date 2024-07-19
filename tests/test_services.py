import json

import pytest
import pandas as pd
from src.services import find_phone_numbers


def test_find_phone_numbers():
    data = {
        'Дата операции': ['2024-04-01', '2024-05-15', '2024-06-20', '2024-07-05'],
        'Сумма операции': [200, 150, 300, 400],
        'Описание': [
            'Я МТС +7 921 11-22-33',
            'Тинькофф Мобайл +7 995 555-55-55',
            'МТС Mobile +7 981 333-44-55',
            'Покупка в магазине'
        ]
    }
    df = pd.DataFrame(data)

    # Ожидаемый результат
    expected = [
        {
            'Дата операции': '2024-04-01',
            'Сумма операции': 200,
            'Описание': 'Я МТС +7 921 11-22-33'
        },
        {
            'Дата операции': '2024-05-15',
            'Сумма операции': 150,
            'Описание': 'Тинькофф Мобайл +7 995 555-55-55'
        },
        {
            'Дата операции': '2024-06-20',
            'Сумма операции': 300,
            'Описание': 'МТС Mobile +7 981 333-44-55'
        }
    ]

    result_json = find_phone_numbers(df)
    result = json.loads(result_json)

    assert result == expected


if __name__ == '__main__':
    pytest.main()
