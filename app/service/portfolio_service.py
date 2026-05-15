from typing import List

from app.db import db
from app.models import Portfolio, User


class UnsupportedPortfolioOperationError(Exception):
    pass


class PortfolioOperationError(Exception):
    pass


def create_portfolio(name: str, description: str, user: User) -> Portfolio:
    if not name or not description or not user:
        raise UnsupportedPortfolioOperationError(
            f'Invalid input[name:{name}, description: {description}, user: {user}]. Please try again.'
        )
    try:
        portfolio = Portfolio(name=name, description=description, user=user)
        db.session.add(portfolio)
        return portfolio
    except Exception as e:
        raise PortfolioOperationError(f"Failed to create portfolio due to error: {str(e)}")


def get_portfolios_by_user(user: User) -> List[Portfolio]:
    try:
        portfolios = db.session.query(Portfolio).filter_by(owner=user.username).all()
        return portfolios
    except Exception as e:
        raise PortfolioOperationError(f"Failed to retrieve portfolios due to error: {str(e)}")


def get_all_portfolios() -> List[Portfolio]:
    try:
        portfolios = db.session.query(Portfolio).all()
        return portfolios
    except Exception as e:
        raise PortfolioOperationError(f"Failed to retrieve portfolios due to error: {str(e)}")


def get_portfolio_by_id(portfolio_id: int) -> Portfolio | None:
    try:
        portfolio = db.session.query(Portfolio).filter_by(id=portfolio_id).one_or_none()
        return portfolio
    except Exception as e:
        raise PortfolioOperationError(f"Failed to retrieve portfolio due to error: {str(e)}")


def delete_portfolio(portfolio_id: int):
    try:
        portfolio = db.session.query(Portfolio).filter_by(id=portfolio_id).one_or_none()
        if not portfolio:
            raise UnsupportedPortfolioOperationError(f'Portfolio with id {portfolio_id} does not exist')
        db.session.delete(portfolio)
    except Exception as e:
        raise PortfolioOperationError(f"Failed to delete portfolio due to error: {str(e)}")

def get_holdings(portfolio_id: int) -> List['Investment']:
    from app.models import Investment
    try:
        holdings = db.session.query(Investment).filter_by(portfolio_id=portfolio_id).all()
        return holdings
    except Exception as e:
        raise PortfolioOperationError(f"Failed to retrieve holdings due to error: {str(e)}")
