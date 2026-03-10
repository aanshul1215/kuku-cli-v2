import pytest
from unittest.mock import patch
from app.models import User, Portfolio
from app.service.portfolio_service import create_portfolio
from app.service.trade_service import execute_purchase_order
from app.service.user_service import create_user
from app.service.alpha_vantage_client import SecurityQuote
from app.service.security_service import SecurityException, get_all_securities, get_security_by_ticker

@pytest.fixture(autouse=True)
def setup(db_session):
    create_user(username="user", password="secret", firstname="Firstname", lastname="Lastname", balance=1000.00)
    user = db_session.query(User).filter_by(username="user").one()
    assert user is not None
    create_portfolio("Test Portfolio", "Test Portfolio Description", user)
    portfolio = db_session.query(Portfolio).filter_by(name="Test Portfolio").one()
    assert portfolio is not None
    return {
        "user": user,
        "portfolio": portfolio
    }

def test_get_security_by_ticker(db_session):
    with patch('app.service.security_service.get_quote') as mock_quote:
        mock_quote.return_value = SecurityQuote(ticker='AAPL', date='2023-01-01', price=150.0, issuer='Apple Inc.')
        security = get_security_by_ticker('AAPL')
        assert security is not None
        assert security['ticker'] == 'AAPL'
        assert security['price'] == 150.0

def test_get_all_securities(db_session):
    with patch('app.service.security_service.get_quote') as mock_quote:
        mock_quote.side_effect = lambda ticker: SecurityQuote(
            ticker=ticker, date='2023-01-01', price=100.0, issuer=f'{ticker} Inc.'
        )
        securities = get_all_securities()
        assert securities is not None
        assert len(securities) >= 3
        tickers = [sec['ticker'] for sec in securities]
        assert 'AAPL' in tickers
        assert 'GOOGL' in tickers
        assert 'MSFT' in tickers

def test_exception_from_get_all_securities(db_session, monkeypatch):
    def mock_get_session_failure(*args, **kwargs):
        raise Exception("Database connection error")
    monkeypatch.setattr(db_session, 'query', mock_get_session_failure)
    with pytest.raises(SecurityException) as e:
        get_all_securities()
    assert "Failed to retrieve securities due to error: Database connection error" in str(e.value)


def test_get_all_securities_uses_transaction_tickers(setup, db_session):
    portfolio = setup['portfolio']
    with patch('app.service.trade_service.get_quote') as mock_trade_quote:
        mock_trade_quote.return_value = SecurityQuote(ticker='AAPL', date='2023-01-01', price=150.0, issuer='Apple Inc.')
        execute_purchase_order(portfolio.id, 'AAPL', 1)
        db_session.commit()

    with patch('app.service.security_service.get_quote') as mock_quote:
        mock_quote.return_value = SecurityQuote(ticker='AAPL', date='2023-01-01', price=150.0, issuer='Apple Inc.')
        securities = get_all_securities()
        assert any(sec['ticker'] == 'AAPL' for sec in securities)