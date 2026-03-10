import os
from typing import List

from app.db import db
from app.models import Investment, Transaction
from app.service.alpha_vantage_client import get_quote


class SecurityException(Exception):
    pass


def _get_ticker_universe() -> list[str]:
    watchlist = os.environ.get('WATCHLIST_TICKERS', 'AAPL,MSFT,GOOGL')
    watchlist_tickers = {ticker.strip().upper() for ticker in watchlist.split(',') if ticker.strip()}
    transaction_tickers = {ticker for (ticker,) in db.session.query(Transaction.ticker).distinct().all()}
    investment_tickers = {ticker for (ticker,) in db.session.query(Investment.ticker).distinct().all()}
    return sorted(watchlist_tickers.union(transaction_tickers).union(investment_tickers))


def get_all_securities() -> List[dict]:
    try:
        securities: list[dict] = []
        for ticker in _get_ticker_universe():
            quote = get_quote(ticker)
            if quote is not None:
                securities.append(
                    {
                        'ticker': quote.ticker,
                        'issuer': quote.issuer,
                        'price': quote.price,
                        'date': quote.date,
                    }
                )
        return securities
    except Exception as e:
        db.session.rollback()
        raise SecurityException(f'Failed to retrieve securities due to error: {str(e)}')


def get_security_by_ticker(ticker: str) -> dict | None:
    try:
        quote = get_quote(ticker.upper())
        if quote is None:
            return None
        return {
            'ticker': quote.ticker,
            'issuer': quote.issuer,
            'price': quote.price,
            'date': quote.date,
        }
    except Exception as e:
        db.session.rollback()
        raise SecurityException(f'Failed to retrieve security due to error: {str(e)}')
