# Проект "Финансовый учет и анализ"

Проект представляет собой программное решение для работы с финансовыми данными, включая анализ трат, 
конвертацию валют, работу с акциями и другими финансовыми инструментами. 
Проект использует Python и различные библиотеки для обработки данных и взаимодействия с API.

# Установка

1. Клонировать репозиторий: git clone <url-репозитория>
2. Установить зависимости: pip install poetry
3. Настройка переменных окружения: Создайте файл .env в корне проекта и добавьте необходимые переменные окружения:
API_KEY=you_api_key


Использование
Проект предоставляет несколько ключевых функций:

Чтение данных из Excel
Модуль для работы с данными из файлов Excel:


Конвертация валюты
Модуль для конвертации валют с использованием внешнего API:


Получение данных о котировках акций
Модуль для получения данных о котировках акций через внешнее API:


Анализ трат по дням недели
Функция для анализа средних трат по дням недели за последние три месяца:


Поиск телефонных номеров в описаниях транзакций
Функция для поиска телефонных номеров в описаниях транзакций:


Тестирование
Для запуска тестов используйте pytest:

pytest

Покрытие кода:

File            statements	missing	 excluded  coverage
src/__init__.py	0	        0	     0	       100%
src/main.py	    9	        9	     0	       0%
src/reports.py	23	        0	     0	       100%
src/services.py	12	        0	     0	       100%
src/utils.py	22	        1	     0	       95%
src/views.py	77	        40	     0	       48%
Total	        143	        50	     0	       65%
Лицензия
MIT License

Этот README файл предоставляет общее представление о проекте и позволяет пользователям 
быстро ознакомиться с его функциональностью и установкой. Вы можете дополнить его дополнительной
информацией о вашем проекте, включая подробности о каждой функции, примеры использования и т.д.






.
├── src
│ ├── __init__.py
│ ├── views.py
│ ├── main.py
│ ├── utils.py
│ ├── reports.py
│ └── services.py
├── data
│ ├── operations.xlsx
├── tests
│ ├── __init__.py
│ ├── test_views.py
│ ├── test_utils.py
│ ├── test_reports.py
│ └── test_services.py
├── .env
├── .flake8
├── .gitignore
├── pyproject.toml
├── poetry.lock
└── README.md