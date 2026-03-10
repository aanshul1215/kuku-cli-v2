from pydantic import BaseModel


class CreatePortfolioRequest(BaseModel):
    username: str
    name: str
    description: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    balance: float


class UpdateBalanceRequest(BaseModel):
    username: str
    new_balance: float


class BuyTradeRequest(BaseModel):
    portfolio_id: int
    ticker: str
    quantity: int | float


class SellTradeRequest(BaseModel):
    portfolio_id: int
    ticker: str
    quantity: int | float


class GrantAccessRequest(BaseModel):
    user_id: str
    role: str


class ErrorResponse(BaseModel):
    error: str
    detail: str