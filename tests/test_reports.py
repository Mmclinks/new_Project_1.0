import pytest
from src.reports import generate_report

def test_generate_report():
    report = generate_report('2023-07-19 14:30:00', 'category')
    assert not report.empty

    report = generate_report('2023-07-19 14:30:00', 'day_of_week')
    assert not report.empty

    report = generate_report('2023-07-19 14:30:00', 'working_day')
    assert not report.empty

    with pytest.raises(ValueError):
        generate_report('2023-07-19 14:30:00', 'invalid_type')
