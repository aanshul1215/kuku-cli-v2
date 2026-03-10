from app.db import db
from app.models import Portfolio, PortfolioAccess

def grant_access(portfolio_id: int, user_id: str, role: str):
    access = PortfolioAccess(portfolio_id=portfolio_id, user_id=user_id, role=role)
    db.session.add(access)

def revoke_access(portfolio_id: int, user_id: str):
    access = db.session.query(PortfolioAccess).filter_by(portfolio_id=portfolio_id, user_id=user_id).first()
    if access:
        db.session.delete(access)

def get_access(portfolio_id: int, user_id: str):
    return db.session.query(PortfolioAccess).filter_by(portfolio_id=portfolio_id, user_id=user_id).first()

def check_access(portfolio_id: int, user_id: str, required_role: str = None):
    # Check if user is owner
    portfolio = db.session.query(Portfolio).filter_by(id=portfolio_id).first()
    if portfolio and portfolio.owner == user_id:
        return True
    access = get_access(portfolio_id, user_id)
    if not access:
        return False
    if required_role == 'manager' and access.role == 'viewer':
        return False
    return True