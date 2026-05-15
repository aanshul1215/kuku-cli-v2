from unittest.mock import patch

import pytest

from app.models import Portfolio, User
from app.service import transaction_service
from app.service.alpha_vantage_client import SecurityQuote
from app.service.portfolio_service import create_portfolio
from app.service.trade_service import (
    InsufficientFundsError,
    TradeExecutionException,
    execute_purchase_order,
    liquidate_investment,
)
from app.service.user_service import create_user


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

# Add tests for trade_service

def test_execute_purchase_order(setup, db_session):
    portfolio = setup["portfolio"]
    transactions = transaction_service.get_transactions_by_portfolio_id(portfolio.id)
    assert len(transactions) == 0
    user = db_session.query(User).filter_by(username="user").one()
    assert user.balance == 1000.00
    with patch('app.service.trade_service.get_quote') as mock_get_quote:
        mock_get_quote.return_value = SecurityQuote(ticker="AAPL", date="2023-01-01", price=150.0, issuer="Apple Inc.")
        execute_purchase_order(portfolio.id, "AAPL", 2)
    db_session.commit()
    user = db_session.query(User).filter_by(username="user").one()
    assert user.balance == 700.00
    user_portfolio = user.portfolios[0]
    assert user_portfolio.investments is not None
    investments = user_portfolio.investments
    assert len(investments) == 1
    investment = investments[0]
    assert investment.ticker == "AAPL"
    assert investment.quantity == 2
    transactions = transaction_service.get_transactions_by_portfolio_id(portfolio.id)
    assert len(transactions) == 1
    assert transactions[0].ticker == "AAPL"
    assert transactions[0].quantity == 2
    assert transactions[0].price == 150.00
    assert transactions[0].transaction_type == "BUY"

def test_execute_purchase_order_insufficient_funds(setup, db_session):
    portfolio = setup["portfolio"]
    with patch('app.service.trade_service.get_quote') as mock_get_quote:
        mock_get_quote.return_value = SecurityQuote(ticker="GOOGL", date="2023-01-01", price=2000.0, issuer="Google")
        with pytest.raises(InsufficientFundsError) as e:
            execute_purchase_order(portfolio.id, "GOOGL", 1)
        assert str(e.value) == "Insufficient funds to complete the purchase."

def test_execute_order_for_nonexistent_portfolio(db_session):
    with patch('app.service.trade_service.get_quote') as mock_get_quote:
        mock_get_quote.return_value = SecurityQuote(ticker="AAPL", date="2023-01-01", price=150.0, issuer="Apple Inc.")
        with pytest.raises(TradeExecutionException) as e:
            execute_purchase_order(999, "AAPL", 1)
        assert "Portfolio with id 999 does not exist." in str(e.value)

def test_liquidate_investment(setup, db_session):
    portfolio = setup["portfolio"]
    # First, add an investment
    with patch('app.service.trade_service.get_quote') as mock_get_quote:
        mock_get_quote.return_value = SecurityQuote(ticker="AAPL", date="2023-01-01", price=150.0, issuer="Apple Inc.")
        execute_purchase_order(portfolio.id, "AAPL", 5)
    db_session.commit()
    # Now liquidate 3
    with patch('app.service.trade_service.get_quote') as mock_get_quote:
        mock_get_quote.return_value = SecurityQuote(ticker="AAPL", date="2023-01-01", price=160.0, issuer="Apple Inc.")
        liquidate_investment(portfolio.id, "AAPL", 3)
    db_session.commit()
    user = db_session.query(User).filter_by(username="user").one()
    assert user.balance == 1000.00 - (5 * 150.0) + (3 * 160.0)  # 250 + 480 = 730
    portfolio = db_session.query(Portfolio).filter_by(id=portfolio.id).one()
    investment = next((inv for inv in portfolio.investments if inv.ticker == "AAPL"), None)
    assert investment.quantity == 2

def test_liquidate_entire_investment(setup, db_session):
    portfolio = setup["portfolio"]
    with patch('app.service.trade_service.get_quote') as mock_get_quote:
        mock_get_quote.return_value = SecurityQuote(ticker="AAPL", date="2023-01-01", price=150.0, issuer="Apple Inc.")
        execute_purchase_order(portfolio.id, "AAPL", 5)
    db_session.commit()
    with patch('app.service.trade_service.get_quote') as mock_get_quote:
        mock_get_quote.return_value = SecurityQuote(ticker="AAPL", date="2023-01-01", price=160.0, issuer="Apple Inc.")
        liquidate_investment(portfolio.id, "AAPL", 5)
    db_session.commit()
    user = db_session.query(User).filter_by(username="user").one()
    assert user.balance == 1000.00 - (5 * 150.0) + (5 * 160.0)  # 250 + 800 = 1050
    portfolio = db_session.query(Portfolio).filter_by(id=portfolio.id).one()
    investment = next((inv for inv in portfolio.investments if inv.ticker == "AAPL"), None)
    assert investment is None
