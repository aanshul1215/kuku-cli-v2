from unittest.mock import patch

AUTH_HEADERS = {'Authorization': 'Bearer fake-token'}


def _mock_admin_token(mock_verify):
    mock_verify.return_value = {'sub': 'admin', 'cognito:username': 'admin'}


def test_get_securities(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch(
        'app.routes.security_routes.security_service.get_all_securities'
    ) as mock_get_all:
        _mock_admin_token(mock_verify)
        mock_get_all.return_value = [{'ticker': 'AAPL', 'issuer': 'Apple Inc.', 'price': 150.0, 'date': '2023-01-01'}]
        response = client.get('/securities/', headers=AUTH_HEADERS)
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert any(item['ticker'] == 'AAPL' for item in data)


def test_get_security_found(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch(
        'app.routes.security_routes.security_service.get_security_by_ticker'
    ) as mock_get_one:
        _mock_admin_token(mock_verify)
        mock_get_one.return_value = {'ticker': 'AAPL', 'issuer': 'Apple Inc.', 'price': 150.0, 'date': '2023-01-01'}
        response = client.get('/securities/AAPL', headers=AUTH_HEADERS)
        assert response.status_code == 200
        payload = response.get_json()
        assert payload['ticker'] == 'AAPL'


def test_get_security_not_found(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch(
        'app.routes.security_routes.security_service.get_security_by_ticker'
    ) as mock_get_one:
        _mock_admin_token(mock_verify)
        mock_get_one.return_value = None
        response = client.get('/securities/NONE', headers=AUTH_HEADERS)
        assert response.status_code == 404
        payload = response.get_json()
        assert 'not found' in payload['error'].lower()


def test_get_security_transactions(client):
    with patch('app.auth.auth.verify_token') as mock_verify:
        _mock_admin_token(mock_verify)
        response = client.get('/securities/AAPL/transactions', headers=AUTH_HEADERS)
        assert response.status_code == 200
        payload = response.get_json()
        assert isinstance(payload, list)


def test_get_portfolios_unauthorized(client):
    response = client.get('/portfolios/')
    assert response.status_code == 403


def test_create_portfolio_authorized(client):
    with patch('app.auth.auth.verify_token') as mock_verify:
        _mock_admin_token(mock_verify)
        response = client.post(
            '/portfolios/',
            headers=AUTH_HEADERS,
            json={'username': 'admin', 'name': 'Test', 'description': 'Test'},
        )
    assert response.status_code == 201
    payload = response.get_json()
    assert 'portfolio_id' in payload


def test_execute_trade_buy_authorized(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch(
        'app.routes.trade_routes.check_access'
    ) as mock_access, patch('app.routes.trade_routes.trade_service.execute_purchase_order') as mock_execute:
        _mock_admin_token(mock_verify)
        mock_access.return_value = True
        response = client.post(
            '/trades/buy',
            headers=AUTH_HEADERS,
            json={'portfolio_id': 1, 'ticker': 'AAPL', 'quantity': 10},
        )
    assert response.status_code == 201
    mock_execute.assert_called_once_with(portfolio_id=1, ticker='AAPL', quantity=10)


def test_execute_trade_sell_authorized(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch(
        'app.routes.trade_routes.check_access'
    ) as mock_access, patch('app.routes.trade_routes.trade_service.liquidate_investment') as mock_liquidate:
        _mock_admin_token(mock_verify)
        mock_access.return_value = True
        response = client.post(
            '/trades/sell',
            headers=AUTH_HEADERS,
            json={'portfolio_id': 1, 'ticker': 'AAPL', 'quantity': 10},
        )
    assert response.status_code == 200
    mock_liquidate.assert_called_once_with(portfolio_id=1, ticker='AAPL', quantity=10)


def test_execute_trade_buy_forbidden(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch('app.routes.trade_routes.check_access') as mock_access:
        _mock_admin_token(mock_verify)
        mock_access.return_value = False
        response = client.post(
            '/trades/buy',
            headers=AUTH_HEADERS,
            json={'portfolio_id': 1, 'ticker': 'AAPL', 'quantity': 10},
        )
    assert response.status_code == 403


def test_execute_trade_sell_forbidden(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch('app.routes.trade_routes.check_access') as mock_access:
        _mock_admin_token(mock_verify)
        mock_access.return_value = False
        response = client.post(
            '/trades/sell',
            headers=AUTH_HEADERS,
            json={'portfolio_id': 1, 'ticker': 'AAPL', 'quantity': 10},
        )
    assert response.status_code == 403


def test_unknown_route_returns_404(client):
    response = client.get('/does-not-exist')
    assert response.status_code == 404
    payload = response.get_json()
    assert payload['error'] == 'Not Found'


def test_grant_portfolio_access_authorized(client):
    with patch('app.auth.auth.verify_token') as mock_verify:
        _mock_admin_token(mock_verify)
        create_resp = client.post(
            '/portfolios/',
            headers=AUTH_HEADERS,
            json={'username': 'admin', 'name': 'Access Test', 'description': 'Access Test'},
        )
        assert create_resp.status_code == 201
        portfolio_id = create_resp.get_json()['portfolio_id']

        grant_resp = client.post(
            f'/portfolios/{portfolio_id}/access',
            headers=AUTH_HEADERS,
            json={'user_id': 'guest_user', 'role': 'viewer'},
        )

    assert grant_resp.status_code == 201
    assert grant_resp.get_json()['message'] == 'Access granted'


def test_manager_cannot_create_or_delete_portfolio(client):
    with patch('app.auth.auth.verify_token') as mock_verify:
        _mock_admin_token(mock_verify)
        create_resp = client.post(
            '/portfolios/',
            headers=AUTH_HEADERS,
            json={'username': 'admin', 'name': 'Owner Portfolio', 'description': 'Owner Portfolio'},
        )
        assert create_resp.status_code == 201
        portfolio_id = create_resp.get_json()['portfolio_id']

    with patch('app.auth.auth.verify_token') as mock_verify:
        mock_verify.return_value = {'sub': 'manager_user', 'cognito:username': 'manager_user'}
        create_forbidden = client.post(
            '/portfolios/',
            headers=AUTH_HEADERS,
            json={'username': 'admin', 'name': 'Should Fail', 'description': 'Should Fail'},
        )
        delete_forbidden = client.delete(f'/portfolios/{portfolio_id}', headers=AUTH_HEADERS)

    assert create_forbidden.status_code == 403
    assert delete_forbidden.status_code == 403


def test_trade_validation_error_returns_422(client):
    with patch('app.auth.auth.verify_token') as mock_verify:
        _mock_admin_token(mock_verify)
        response = client.post(
            '/trades/buy',
            headers=AUTH_HEADERS,
            json={'portfolio_id': 'bad', 'ticker': 'AAPL', 'quantity': 10},
        )
    assert response.status_code == 422
    payload = response.get_json()
    assert payload['error'] == 'Validation error'

def test_get_my_portfolios_authorized(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch('app.routes.portfolio_routes.user_service.get_user_by_username') as mock_user, patch('app.routes.portfolio_routes.portfolio_service.get_portfolios_by_user') as mock_portfolios:
        _mock_admin_token(mock_verify)
        mock_user.return_value = 'some_user'
        from app.models import Portfolio
        mock_portfolios.return_value = [Portfolio(name='Test', description='Test')]
        response = client.get('/portfolios/me', headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_my_portfolios_no_user(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch('app.routes.portfolio_routes.user_service.get_user_by_username') as mock_user:
        _mock_admin_token(mock_verify)
        mock_user.return_value = None
        response = client.get('/portfolios/me', headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_portfolio_holdings_authorized(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch('app.routes.portfolio_routes.check_access') as mock_access, patch('app.routes.portfolio_routes.portfolio_service.get_portfolio_by_id') as mock_get, patch('app.routes.portfolio_routes.portfolio_service.get_holdings') as mock_holdings:
        _mock_admin_token(mock_verify)
        mock_access.return_value = True
        mock_get.return_value = 'some_portfolio'
        from app.models import Investment
        mock_holdings.return_value = [Investment(ticker='AAPL', quantity=10, portfolio_id=1)]
        response = client.get('/portfolios/1/holdings', headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_portfolio_holdings_forbidden(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch('app.routes.portfolio_routes.check_access') as mock_access:
        _mock_admin_token(mock_verify)
        mock_access.return_value = False
        response = client.get('/portfolios/1/holdings', headers=AUTH_HEADERS)
    assert response.status_code == 403

def test_get_portfolio_holdings_not_found(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch('app.routes.portfolio_routes.check_access') as mock_access, patch('app.routes.portfolio_routes.portfolio_service.get_portfolio_by_id') as mock_get:
        _mock_admin_token(mock_verify)
        mock_access.return_value = True
        mock_get.return_value = None
        response = client.get('/portfolios/1/holdings', headers=AUTH_HEADERS)
    assert response.status_code == 404

def test_get_portfolio_transactions_authorized(client):
    with patch('app.auth.auth.verify_token') as mock_verify, patch('app.routes.portfolio_routes.check_access') as mock_access, patch('app.routes.portfolio_routes.portfolio_service.get_portfolio_by_id') as mock_get, patch('app.routes.portfolio_routes.transaction_service.get_transactions_by_portfolio_id') as mock_transactions:
        _mock_admin_token(mock_verify)
        mock_access.return_value = True
        mock_get.return_value = 'some_portfolio'
        import datetime

        from app.models import Transaction
        t = Transaction(username='admin', portfolio_id=1, ticker='AAPL', transaction_type='BUY', quantity=10, price=100.0, date_time=datetime.datetime.now())
        t.transaction_id = 1
        mock_transactions.return_value = [t]
        response = client.get('/portfolios/1/transactions', headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)