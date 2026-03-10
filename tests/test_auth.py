import pytest
import jwt
from unittest.mock import patch, MagicMock
from app.auth.auth import verify_token, require_auth, AuthError

def test_verify_token_valid():
    with patch('app.auth.auth._get_jwks_client') as mock_jwks, \
         patch('app.auth.auth.jwt.decode') as mock_decode:
        mock_key = MagicMock()
        mock_key.key = "key"
        mock_jwks.return_value.get_signing_key_from_jwt.return_value = mock_key
        mock_decode.return_value = {"sub": "user123", "cognito:username": "user"}
        result = verify_token("valid_token")
        assert result == {"sub": "user123", "cognito:username": "user"}

def test_verify_token_expired():
    with patch('app.auth.auth._get_jwks_client') as mock_jwks, \
         patch('app.auth.auth.jwt.decode') as mock_decode:
        mock_decode.side_effect = jwt.ExpiredSignatureError()
        with pytest.raises(AuthError):
            verify_token("expired_token")

def test_verify_token_invalid():
    with patch('app.auth.auth._get_jwks_client') as mock_jwks, \
         patch('app.auth.auth.jwt.decode') as mock_decode:
        mock_decode.side_effect = jwt.InvalidTokenError()
        with pytest.raises(AuthError):
            verify_token("invalid_token")

def test_require_auth_valid(app):
    with app.test_request_context('/test', headers={'Authorization': 'Bearer token'}):
        with patch('app.auth.auth.verify_token') as mock_verify:
            mock_verify.return_value = {"sub": "user123", "cognito:username": "user"}
            decorator = require_auth(lambda: "success")
            result = decorator()
            assert result == "success"

def test_require_auth_missing_header(app):
    with app.test_request_context('/test'):
        decorator = require_auth(lambda: "success")
        response, status = decorator()
        assert status == 403
        assert 'Authorization header missing' in response['error']

def test_require_auth_invalid_token(app):
    with app.test_request_context('/test', headers={'Authorization': 'Bearer invalid'}):
        with patch('app.auth.auth.verify_token') as mock_verify:
            mock_verify.side_effect = AuthError("Invalid token")
            decorator = require_auth(lambda: "success")
            response, status = decorator()
            assert status == 403
            assert 'Invalid token' in response['error']