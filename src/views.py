import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Union

import pandas as pd
import requests
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

from src.utils import calculate_cashback, get_greeting, read_transactions_from_excel

# Загрузка переменных окружения из .env файла
load_dotenv()

# Создание объекта Blueprint для маршрутов
views = Blueprint("views", __name__)


@views.route("/main", methods=["GET"])
def main_page_analysis():
    """
    Обрабатывает GET-запрос на основной маршрут '/main' и возвращает анализ данных на основе переданной даты.

    Параметры запроса:
    - date (str): Дата в формате "YYYY-MM-DD HH:MM:SS", по которой производится анализ.

    Возвращает:
    - JSON: Объект с результатами анализа, включающий приветствие, информацию о картах, топ-5 транзакций,
      курсы валют и цены акций.
    - 400 Bad Request: Если параметр даты отсутствует или имеет неверный формат.
    - 500 Internal Server Error: Если возникла ошибка при чтении данных транзакций.
    """
    date_str = request.args.get("date")
    if not date_str:
        return jsonify({"error": "Параметр даты отсутствует"}), 400

    try:
        current_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Неверный формат даты"}), 400

    greeting = get_greeting(current_date)

    start_date = current_date.replace(day=1)
    end_date = current_date

    df = read_transactions_from_excel("data/operations.xlsx")
    if df is None:
        return jsonify({"error": "Не удалось прочитать данные транзакций"}), 500

    df["Дата операции"] = pd.to_datetime(df["Дата операции"])
    df_filtered = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    cards_info = []
    for last_digits, group in df_filtered.groupby("Номер карты"):
        total_spent = group["Сумма операции"].sum()
        cashback = calculate_cashback(total_spent)
        cards_info.append(
            {
                "last_digits": str(last_digits)[-4:],  # Последние 4 цифры номера карты
                "total_spent": total_spent,  # Общая сумма расходов
                "cashback": cashback,  # Рассчитанный кэшбэк
            }
        )

    top_transactions = df_filtered.nlargest(5, "Сумма операции")[
        ["Дата операции", "Сумма операции", "Категория", "Описание"]
    ].to_dict(orient="records")

    try:
        api_key = os.getenv("API_KEY")
        currency_rates = get_currency_rates(api_key)
    except Exception as e:
        logging.error(f"Ошибка при получении курсов валют: {e}")
        currency_rates = []

    try:
        stock_prices = get_stock_prices()
    except Exception as e:
        logging.error(f"Ошибка при получении цен акций: {e}")
        stock_prices = []

    result = {
        "greeting": greeting,
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return jsonify(result)


def get_currency_rates(api_key: str) -> str:
    """
    Получает курсы валют по отношению к рублю с использованием заданного API ключа.

    Параметры:
    - api_key (str): API ключ для доступа к сервису курсов валют.

    Возвращает:
    - str: Список словарей с валютами и их курсами по отношению к рублю в формате JSON.
    """
    url = f"https://api.exchangerate-api.com/v4/latest/RUB?apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешности запроса
        data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching currency rates: {e}")
        return json.dumps({"error": "Failed to fetch currency rates"}, ensure_ascii=False)

    try:
        with open("src/user_settings.json", "r") as file:
            user_settings = json.load(file)
        user_currencies = user_settings.get("user_currencies", [])
        rates = [{"currency": cur, "rate": data["rates"].get(cur, "N/A")} for cur in user_currencies]
        return json.dumps(rates, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error processing user settings: {e}")
        return json.dumps({"error": "Failed to process user settings"}, ensure_ascii=False)


def get_stock_prices() -> List[Dict[str, Union[str, float]]]:
    """
    Получает текущие цены акций по символам из файла настроек пользователя.

    Возвращает:
    - list: Список словарей с символами акций и их текущими ценами.
    """
    with open("src/user_settings.json", "r") as file:
        user_settings = json.load(file)
    user_stocks = user_settings.get("user_stocks", [])
    prices = []
    api_key = os.getenv("API_KEY")  # Использование переменной окружения для API ключа
    for stock in user_stocks:
        response = requests.get(f"https://finnhub.io/api/v1/quote?symbol={stock}&token={api_key}")
        data = response.json()
        prices.append({"stock": stock, "price": data["c"]})
    return prices
