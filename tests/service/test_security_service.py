import pytest
from unittest.mock import patch
from app.models import User, Portfolio
from app.service.portfolio_service import create_portfolio
from app.service.trade_service import execute_purchase_order, InsufficientFundsError
from app.service.user_service import create_user
from app.service import transaction_service
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

# Add tests for trade_service

def test_get_security_by_ticker(db_session):
    security = get_security_by_ticker("AAPL")
    assert security is not None
    assert security.ticker == "AAPL"
    assert security.price == 150.00

def test_get_all_securities(db_session):
    securities = get_all_securities()
    assert securities is not None
    assert len(securities) == 3
    tickers = [sec.ticker for sec in securities]
    assert "AAPL" in tickers
    assert "GOOGL" in tickers
    assert "MSFT" in tickers

def test_exception_from_get_all_securities(db_session, monkeypatch):
    def mock_get_session_failure(*args, **kwargs):
        raise Exception("Database connection error")
    monkeypatch.setattr(db_session, 'query', mock_get_session_failure)
    with pytest.raises(SecurityException) as e:
        get_all_securities()
    assert "Failed to retrieve securities due to error: Database connection error" in str(e.value)