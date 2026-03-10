from pydantic import BaseModel


class CreatePortfolioRequest(BaseModel):
    username: str
    name: str
    description: str


class BuyTradeRequest(BaseModel):
    portfolio_id: int
    ticker: str
    quantity: int


class SellTradeRequest(BaseModel):
    portfolio_id: int
    ticker: str
    quantity: int


class GrantAccessRequest(BaseModel):
    user_id: str
    role: str