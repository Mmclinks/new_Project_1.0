import pytest
from src.services import get_cashback_categories, get_investment_piggy_bank, simple_search, search_by_phone, \
    search_transfers_to_individuals
from src.utils import load_data


@pytest.fixture
def transactions():
    return load_data('data/operations.xlsx')


def test_get_cashback_categories(transactions):
    cashback = get_cashback_categories(transactions)
    assert not cashback.empty


def test_get_investment_piggy_bank(transactions):
    piggy_bank = get_investment_piggy_bank(transactions)
    assert not piggy_bank.empty


def test_simple_search(transactions):
    search_result = simple_search(transactions, 'example_query')
    assert not search_result.empty


def test_search_by_phone(transactions):
    phone_search = search_by_phone(transactions, '1234567890')
    assert not phone_search.empty


def test_search_transfers_to_individuals(transactions):
    transfers = search_transfers_to_individuals(transactions)
    assert not transfers.empty
