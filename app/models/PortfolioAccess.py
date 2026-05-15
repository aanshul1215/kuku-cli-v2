from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import db


class PortfolioAccess(db.Model):
    __tablename__ = 'portfolio_access'

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.id'), nullable=False)
    user_id = Column(String(50), nullable=False)  # Assuming user_id is username or similar
    role = Column(String(20), nullable=False)  # 'viewer' or 'manager'

    portfolio = relationship('Portfolio', backref='accesses')

    def __to_dict__(self):
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'user_id': self.user_id,
            'role': self.role,
        }
