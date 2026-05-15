import pytest
from pydantic import ValidationError

from app.schemas import (
    BuyTradeRequest,
    CreatePortfolioRequest,
    CreateUserRequest,
    ErrorResponse,
    GrantAccessRequest,
    SellTradeRequest,
    UpdateBalanceRequest,
)


def test_buy_trade_request_valid():
    req = BuyTradeRequest(portfolio_id=1, ticker="AAPL", quantity=10)
    assert req.portfolio_id == 1
    assert req.ticker == "AAPL"
    assert req.quantity == 10

def test_buy_trade_request_invalid():
    with pytest.raises(ValidationError):
        BuyTradeRequest(portfolio_id="invalid", ticker="AAPL", quantity=10)


def test_buy_trade_request_float_quantity_valid():
    req = BuyTradeRequest(portfolio_id=1, ticker='AAPL', quantity=10.0)
    assert req.quantity == 10.0

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


def test_create_user_request_valid():
    req = CreateUserRequest(username='u1', password='p', firstname='A', lastname='B', balance=100.0)
    assert req.username == 'u1'


def test_update_balance_request_valid():
    req = UpdateBalanceRequest(username='u1', new_balance=200.0)
    assert req.new_balance == 200.0


def test_error_response_schema_valid():
    err = ErrorResponse(error='Validation error', detail='details here')
    assert err.error == 'Validation error'


def test_create_user_request_invalid_balance():
    with pytest.raises(ValidationError):
        CreateUserRequest(username='u1', password='p', firstname='A', lastname='B', balance='bad')
