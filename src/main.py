import json
from datetime import datetime
from src.utils import load_transactions, get_transactions_in_date_range, calculate_cashback, get_top_transactions, \
    load_user_settings
from src.views import get_currency_rates, get_stock_prices, get_greeting

from dotenv import load_dotenv


# Загрузка переменных из .env-файла
load_dotenv()

def generate_json_response(input_date, df, currency_api_url, stock_api_url, user_settings):
    transactions_df = get_transactions_in_date_range(df, input_date)
    current_time = datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S')

    response = {
        'greeting': get_greeting(current_time),
        'top_transactions': get_top_transactions(transactions_df),
        'currency_rates': get_currency_rates(currency_api_url, user_settings['user_currencies']),
        'stock_prices': get_stock_prices(stock_api_url, user_settings['user_stocks'])
    }

    return json.dumps(response, ensure_ascii=False, indent=4)


def main():
    input_date = '2024-07-19 12:00:00'
    transactions_df = load_transactions('data/operations.xlsx')
    user_settings = load_user_settings('user_settings.json')

    # Определите переменные
    api_key = 'ALPHA_VANTAGE_API_KEY'
    stock = 'AAPL'  # Или другой тикер акций

    currency_api_url = 'https://api.exchangerate-api.com/v4/latest/USD'
    stock_api_url = (
        f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
        f'&symbol=IBM&interval=5min&outputsize=full&apikey={api_key}'
    )

    json_response = generate_json_response(input_date, transactions_df, currency_api_url, stock_api_url, user_settings)
    print(json_response)


if __name__ == '__main__':
    main()
