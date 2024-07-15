# Проект "Финансовый учет и анализ"

Проект представляет собой программное решение для работы с финансовыми данными, включая анализ трат, 
конвертацию валют, работу с акциями и другими финансовыми инструментами. 
Проект использует Python и различные библиотеки для обработки данных и взаимодействия с API.

# Установка
Для установки необходимо выполнить следующие шаги:
1. Клонировать репозиторий: git clone <url-репозитория>
2. Установить зависимости: pip install poetry
3. Настройка переменных окружения: Создайте файл .env в корне проекта и добавьте необходимые переменные окружения:
EXCEL_FILE_PATH=path/to/excel/file.xlsx
USER_SETTINGS_FILE_PATH=path/to/user_settings.json
CURRENCY_API_URL=https://api.exchangerate-api.com/v4/latest/
STOCK_API_URL=https://api.example.com/stock/
Эти переменные будут использоваться для доступа к файлам Excel, настроек пользователя, API курсов валют и акций 
соответственно.
Использование
Проект предоставляет несколько ключевых функций:

Чтение данных из Excel

Модуль для работы с данными из файлов Excel:

from src.utils import read_excel_data
Пример использования
data = read_excel_data('operations.xlsx', '2024-07-13 12:00:00')
print(data)

Конвертация валюты
Модуль для конвертации валют с использованием внешнего API:

from src.currency import convert_currency
Пример использования
amount_usd = convert_currency(100, 'USD', 'EUR')
print(f"100 USD = {amount_usd} EUR")

Получение данных о котировках акций
Модуль для получения данных о котировках акций через внешнее API:

from src.stock import get_stock_price
Пример использования
price = get_stock_price('AAPL')
print(f"Текущая цена акций Apple: ${price}")

Анализ трат по дням недели
Функция для анализа средних трат по дням недели за последние три месяца:

from src.analysis import spending_by_weekday
Пример использования
data = spending_by_weekday(transactions_df, date='2024-07-13')
print(data)

Поиск телефонных номеров в описаниях транзакций
Функция для поиска телефонных номеров в описаниях транзакций:

from src.analysis import search_phone_numbers
Пример использования
phone_transactions = search_phone_numbers(transactions_df)
print(phone_transactions)

Тестирование
Для запуска тестов используйте pytest:

pytest

Покрытие кода:

Лицензия
MIT License

Этот README файл предоставляет общее представление о проекте и позволяет пользователям 
быстро ознакомиться с его функциональностью и установкой. Вы можете дополнить его дополнительной
информацией о вашем проекте, включая подробности о каждой функции, примеры использования и т.д.






.
├── src
│ ├── __init__.py
│ ├── views.py
│ ├── reports.py
│ └── services.py
├── data
│ ├── operations.xlsx
├── tests
│ ├── __init__.py
│ ├── test_views.py
│ ├── test_reports.py
│ └── test_services.py
├── .env
├── .flake8
├── .gitignore
├── pyproject.toml
├── poetry.lock
└── README.md