import os
from dataclasses import dataclass

import requests
from flask import current_app

@dataclass
class SecurityQuote:
    ticker: str
    date: str
    price: float
    issuer: str

def _get_api_key() -> str:
    return os.environ.get('ALPHA_VANTAGE_API_KEY')

def get_company_name(ticker: str) -> str | None:
    cache = current_app.cache
    cache_key = f"company_name:{ticker}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    api_key = _get_api_key()
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        name = data.get('Name')
        if name:
            cache.set(cache_key, name)
            return name
    return None

def get_price_data(ticker: str) -> dict | None:
    cache = current_app.cache
    cache_key = f"price_data:{ticker}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    api_key = _get_api_key()
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        time_series = data.get('Time Series (Daily)')
        if time_series:
            latest_date = max(time_series.keys())
            latest_data = time_series[latest_date]
            price_data = {
                'date': latest_date,
                'open': float(latest_data['1. open']),
                'high': float(latest_data['2. high']),
                'low': float(latest_data['3. low']),
                'close': float(latest_data['4. close']),
                'volume': int(latest_data['5. volume'])
            }
            cache.set(cache_key, price_data)
            return price_data
    return None

def get_quote(ticker: str) -> SecurityQuote | None:
    name = get_company_name(ticker)
    price_data = get_price_data(ticker)
    if name and price_data:
        return SecurityQuote(
            ticker=ticker,
            date=price_data['date'],
            price=price_data['close'],
            issuer=name
        )
    return None