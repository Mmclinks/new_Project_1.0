import json
import unittest

from src.services import search_by_phone


class TestSearchByPhone(unittest.TestCase):

    def setUp(self):
        # Создание тестовых данных
        self.transactions = [
            {"Дата операции": "2024-07-01", "Описание": "Оплата по телефону +1234567890", "Сумма операции": 100},
            {"Дата операции": "2024-07-02", "Описание": "Оплата по телефону +0987654321", "Сумма операции": 200},
            {"Дата операции": "2024-07-03", "Описание": "Покупка товаров", "Сумма операции": 300},
            {"Дата операции": "2024-07-04", "Описание": "Перевод на карту +1234567890", "Сумма операции": 400}
        ]

    def test_valid_phone_number(self):
        phone_number = r"\+1234567890"
        expected_output = json.dumps([
            {"Дата операции": "2024-07-01", "Описание": "Оплата по телефону +1234567890", "Сумма операции": 100},
            {"Дата операции": "2024-07-04", "Описание": "Перевод на карту +1234567890", "Сумма операции": 400}
        ], ensure_ascii=False)

        result = search_by_phone(self.transactions, phone_number)
        self.assertEqual(result, expected_output)

    def test_no_matching_phone_number(self):
        phone_number = r"\+1111111111"
        expected_output = json.dumps([], ensure_ascii=False)

        result = search_by_phone(self.transactions, phone_number)
        self.assertEqual(result, expected_output)

    def test_invalid_phone_number_pattern(self):
        phone_number = r"(\+123"  # неправильный шаблон регулярного выражения
        result = search_by_phone(self.transactions, phone_number)
        self.assertIn("error", json.loads(result))

    def test_empty_description(self):
        phone_number = r"\+1234567890"
        self.transactions.append({"Дата операции": "2024-07-05", "Описание": "", "Сумма операции": 500})
        expected_output = json.dumps([
            {"Дата операции": "2024-07-01", "Описание": "Оплата по телефону +1234567890", "Сумма операции": 100},
            {"Дата операции": "2024-07-04", "Описание": "Перевод на карту +1234567890", "Сумма операции": 400}
        ], ensure_ascii=False)

        result = search_by_phone(self.transactions, phone_number)
        self.assertEqual(result, expected_output)
