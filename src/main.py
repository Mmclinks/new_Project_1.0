import pandas as pd
from flask import Flask, request, jsonify
from src.services import (
    analyze_cashback_categories,
    investment_bank,
    simple_search,
    search_phone_numbers,
    search_personal_transfers,
    load_data
)

app = Flask(__name__)

data_file_path = 'data/operations.xlsx'
data = load_data(data_file_path)

@app.route('/cashback_analysis', methods=['GET'])
def cashback_analysis():
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    result = analyze_cashback_categories(data, year, month)
    return jsonify(result)

@app.route('/investment_bank', methods=['GET'])
def invest_bank():
    month = request.args.get('month')
    limit = int(request.args.get('limit'))
    transactions = data.to_dict(orient='records')
    result = investment_bank(month, transactions, limit)
    return jsonify({"total_investment": result})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    result = simple_search(data, query)
    return jsonify(result)

@app.route('/search_phone_numbers', methods=['GET'])
def phone_numbers():
    result = search_phone_numbers(data)
    return jsonify(result)

@app.route('/search_personal_transfers', methods=['GET'])
def personal_transfers():
    result = search_personal_transfers(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
