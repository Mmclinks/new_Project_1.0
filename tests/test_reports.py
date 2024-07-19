import pytest
import pandas as pd
from src.reports import spending_by_weekday


def test_spending_by_weekday():
    data = {
        'Дата операции': ['2024-04-01', '2024-05-15', '2024-06-20', '2024-07-05'],
        'Сумма операции': [200, 150, 300, 400]
    }
    df = pd.DataFrame(data)

    # Переопределяем текущую дату для теста
    result = spending_by_weekday(df, '2024-07-01')

    # Ожидаемый результат
    expected = pd.DataFrame({
        'Weekday': ['Monday', 'Saturday', 'Tuesday'],
        'Средние траты': [200.0, 400.0, 300.0]
    }).sort_values(by='Weekday').reset_index(drop=True)

    pd.testing.assert_frame_equal(result.sort_values(by='Weekday').reset_index(drop=True), expected)


if __name__ == '__main__':
    pytest.main()
