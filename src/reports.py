import json
import logging
from datetime import datetime

import pandas as pd


def spending_by_weekday(df: pd.DataFrame, date_str: str) -> str:
    """
    Генерирует отчет о расходах по дням недели за месяц, в котором находится указанная дата.

    Параметры:
    df (pd.DataFrame): DataFrame, содержащий данные о транзакциях. Ожидается, что в нем есть следующие колонки:
                       - 'Дата операции': даты операций (формат 'YYYY-MM-DD HH:MM:SS')
                       - 'Сумма операции': сумма операции
    date_str (str): Дата в формате 'YYYY-MM-DD HH:MM:SS', на основе которой определяется месяц для отчета.

    Возвращает:
    str: JSON строка, содержащая отчет о расходах по дням недели. Если данные отсутствуют или произошла ошибка,
         возвращается JSON строка с сообщением об ошибке.
    """
    try:
        # Преобразование строки даты в объект datetime
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        start_date = date.replace(day=1)

        # Убедитесь, что колонка 'Дата операции' имеет тип datetime
        if not pd.api.types.is_datetime64_any_dtype(df["Дата операции"]):
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")

        # Фильтрация данных по дате
        filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= date)]

        # Обработка возможного пустого DataFrame
        if filtered_df.empty:
            return json.dumps([], ensure_ascii=False)

        # Добавление колонки с днем недели
        filtered_df["День недели"] = filtered_df["Дата операции"].dt.day_name()
        report = filtered_df.groupby("День недели").agg({"Сумма операции": "sum"}).reset_index()

        # Определение порядка дней недели
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        report["День недели"] = pd.Categorical(report["День недели"], categories=days_order, ordered=True)
        report = report.sort_values("День недели")

        # Преобразование в JSON строку
        result = report.to_dict(orient="records")
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        # Логирование ошибки и возврат сообщения об ошибке
        logging.error(f"Ошибка при генерации отчета о расходах по дням недели: {e}")
        return json.dumps({"error": "Не удалось сгенерировать отчет"})
