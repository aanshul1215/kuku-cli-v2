import os
import jwt
import requests
from flask import g, request
from functools import wraps
from jwt import PyJWKClient

class AuthError(Exception):
    pass

def _get_jwks_client():
    jwks_url = os.environ.get('COGNITO_JWKS_URL')
    return PyJWKClient(jwks_url)

def _get_cognito_config():
    user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')
    region = os.environ.get('COGNITO_REGION')
    expected_issuer = os.environ.get('COGNITO_ISSUER')
    if not expected_issuer and user_pool_id and region:
        expected_issuer = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}'

    return {
        'user_pool_id': user_pool_id,
        'app_client_id': os.environ.get('COGNITO_APP_CLIENT_ID'),
        'region': region,
        'issuer': expected_issuer,
    }

def verify_token(token):
    try:
        cognito_config = _get_cognito_config()
        jwks_client = _get_jwks_client()
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=['RS256'],
            audience=cognito_config['app_client_id'],
            issuer=cognito_config['issuer'],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthError('Invalid token')
    except Exception as e:
        raise AuthError(f'Token verification failed: {str(e)}')

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return {'error': 'Authorization header missing or invalid'}, 403
        token = auth_header.split(' ')[1]
        try:
            payload = verify_token(token)
            g.user_id = payload.get('sub')  # Cognito sub is user ID
            g.username = payload.get('cognito:username')  # Or email, depending on config
        except AuthError as e:
            return {'error': str(e)}, 403
        return f(*args, **kwargs)
    return decorated_function