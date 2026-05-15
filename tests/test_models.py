from app import create_app
from app.models import Investment, Security, Transaction, User


def test_create_app():
    app = create_app()
    assert app is not None
    assert app.name == 'app'


def test_user_str():
    user = User(username='test', password='pass', firstname='Test', lastname='User', balance=100.0)
    # Since portfolios is a relationship, it might be empty
    expected = "<User: username='test'; name='Test User'; #portfolios=0; balance=100.0)"
    assert str(user) == expected


def test_security_str():
    security = Security(ticker='AAPL', issuer='Apple Inc.', price=150.0)
    expected = '<Security: ticker=AAPL; issuer=Apple Inc.; price=150.0; #investments=0>'
    assert str(security) == expected


def test_transaction_str():
    import datetime
    dt = datetime.datetime.now()
    transaction = Transaction(username='test', portfolio_id=1, ticker='AAPL', transaction_type='BUY', quantity=10, price=150.0, date_time=dt)
    expected = f'<Transaction: id=None; user=test; portfolio_id=1; ticker=AAPL; type=BUY; quantity=10; price=150.0; date_time={dt}>'
    assert str(transaction) == expected


def test_investment_str():
    investment = Investment(quantity=10, ticker='AAPL')
    expected = '<Investment: id=None; portfolio id=None; quantity=10; portfolio=None>'
    assert str(investment) == expected
