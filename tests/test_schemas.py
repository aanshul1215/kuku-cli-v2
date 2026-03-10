import pytest
from pydantic import ValidationError
from app.schemas import BuyTradeRequest, SellTradeRequest, CreatePortfolioRequest, GrantAccessRequest

def test_buy_trade_request_valid():
    req = BuyTradeRequest(portfolio_id=1, ticker="AAPL", quantity=10)
    assert req.portfolio_id == 1
    assert req.ticker == "AAPL"
    assert req.quantity == 10

def test_buy_trade_request_invalid():
    with pytest.raises(ValidationError):
        BuyTradeRequest(portfolio_id="invalid", ticker="AAPL", quantity=10)

def test_sell_trade_request_valid():
    req = SellTradeRequest(portfolio_id=1, ticker="AAPL", quantity=10)
    assert req.portfolio_id == 1
    assert req.ticker == "AAPL"
    assert req.quantity == 10

def test_create_portfolio_request_valid():
    req = CreatePortfolioRequest(username="user", name="Portfolio", description="Desc")
    assert req.username == "user"
    assert req.name == "Portfolio"
    assert req.description == "Desc"

def test_grant_access_request_valid():
    req = GrantAccessRequest(user_id="user", role="viewer")
    assert req.user_id == "user"
    assert req.role == "viewer"