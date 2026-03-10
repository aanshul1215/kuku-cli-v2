import pytest
from unittest.mock import patch, MagicMock
from app.service.alpha_vantage_client import get_company_name, get_price_data, get_quote, SecurityQuote

@pytest.fixture
def mock_current_app():
    with patch('app.service.alpha_vantage_client.current_app') as mock_app:
        mock_cache = MagicMock()
        mock_app.cache = mock_cache
        yield mock_app, mock_cache

def test_get_company_name_cached(mock_current_app):
    mock_app, mock_cache = mock_current_app
    mock_cache.get.return_value = "Apple Inc."
    result = get_company_name("AAPL")
    assert result == "Apple Inc."
    mock_cache.get.assert_called_once_with("company_name:AAPL")
    mock_cache.set.assert_not_called()

def test_get_company_name_api_success(mock_current_app):
    mock_app, mock_cache = mock_current_app
    mock_cache.get.return_value = None
    with patch('app.service.alpha_vantage_client.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"Name": "Apple Inc."}
        mock_get.return_value = mock_response
        result = get_company_name("AAPL")
        assert result == "Apple Inc."
        mock_cache.set.assert_called_once_with("company_name:AAPL", "Apple Inc.")

def test_get_company_name_api_failure(mock_current_app):
    mock_app, mock_cache = mock_current_app
    mock_cache.get.return_value = None
    with patch('app.service.alpha_vantage_client.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        result = get_company_name("INVALID")
        assert result is None

def test_get_price_data_cached(mock_current_app):
    mock_app, mock_cache = mock_current_app
    cached_data = {"date": "2023-01-01", "close": 150.0}
    mock_cache.get.return_value = cached_data
    result = get_price_data("AAPL")
    assert result == cached_data
    mock_cache.set.assert_not_called()

def test_get_price_data_api_success(mock_current_app):
    mock_app, mock_cache = mock_current_app
    mock_cache.get.return_value = None
    with patch('app.service.alpha_vantage_client.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Time Series (Daily)": {
                "2023-01-01": {
                    "1. open": "149.0",
                    "2. high": "151.0",
                    "3. low": "148.0",
                    "4. close": "150.0",
                    "5. volume": "1000000"
                }
            }
        }
        mock_get.return_value = mock_response
        result = get_price_data("AAPL")
        expected = {
            "date": "2023-01-01",
            "open": 149.0,
            "high": 151.0,
            "low": 148.0,
            "close": 150.0,
            "volume": 1000000
        }
        assert result == expected
        mock_cache.set.assert_called_once()

def test_get_price_data_api_failure(mock_current_app):
    mock_app, mock_cache = mock_current_app
    mock_cache.get.return_value = None
    with patch('app.service.alpha_vantage_client.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        result = get_price_data("INVALID")
        assert result is None

def test_get_quote_success(mock_current_app):
    mock_app, mock_cache = mock_current_app
    with patch('app.service.alpha_vantage_client.get_company_name') as mock_name, \
         patch('app.service.alpha_vantage_client.get_price_data') as mock_price:
        mock_name.return_value = "Apple Inc."
        mock_price.return_value = {"date": "2023-01-01", "close": 150.0}
        result = get_quote("AAPL")
        assert result == SecurityQuote(ticker="AAPL", date="2023-01-01", price=150.0, issuer="Apple Inc.")

def test_get_quote_failure(mock_current_app):
    mock_app, mock_cache = mock_current_app
    with patch('app.service.alpha_vantage_client.get_company_name') as mock_name, \
         patch('app.service.alpha_vantage_client.get_price_data') as mock_price:
        mock_name.return_value = None
        mock_price.return_value = {"date": "2023-01-01", "close": 150.0}
        result = get_quote("INVALID")
        assert result is None