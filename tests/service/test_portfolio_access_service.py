import app.service.user_service as user_service
from app.models import Portfolio
from app.service.portfolio_access_service import check_access, grant_access


def test_check_access_owner(db_session):
    portfolio = Portfolio(name='Owner Portfolio', description='Owner Portfolio', owner='admin')
    db_session.add(portfolio)
    db_session.commit()

    assert check_access(portfolio.id, 'admin') is True


def test_check_access_no_access(db_session):
    user_service.create_user('guest_user', 'pwd', 'Guest', 'User', 100.0)
    portfolio = Portfolio(name='No Access Portfolio', description='No Access Portfolio', owner='admin')
    db_session.add(portfolio)
    db_session.commit()

    assert check_access(portfolio.id, 'guest_user') is False


def test_check_access_viewer_not_manager(db_session):
    user_service.create_user('viewer_user', 'pwd', 'Viewer', 'User', 100.0)
    portfolio = Portfolio(name='Viewer Portfolio', description='Viewer Portfolio', owner='admin')
    db_session.add(portfolio)
    db_session.commit()

    grant_access(portfolio.id, 'viewer_user', 'viewer')
    db_session.commit()

    assert check_access(portfolio.id, 'viewer_user') is True
    assert check_access(portfolio.id, 'viewer_user', 'manager') is False


def test_check_access_manager_allowed(db_session):
    user_service.create_user('manager_user', 'pwd', 'Manager', 'User', 100.0)
    portfolio = Portfolio(name='Manager Portfolio', description='Manager Portfolio', owner='admin')
    db_session.add(portfolio)
    db_session.commit()

    grant_access(portfolio.id, 'manager_user', 'manager')
    db_session.commit()

    assert check_access(portfolio.id, 'manager_user', 'manager') is True
