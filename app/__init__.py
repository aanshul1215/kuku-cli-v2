from flask import Flask, jsonify
from flask_caching import Cache
from pydantic import ValidationError

from app.config import get_config
from app.db import db
from app.routes import portfolio_bp, security_bp, trade_bp, user_bp

cache = Cache()


def create_app(config_name=None):
    try:
        app = Flask(__name__)
        config = get_config(config_name)
        app.config.from_object(config)

        # register extensions
        db.init_app(app)

        # register blueprints
        app.register_blueprint(user_bp, url_prefix='/users')
        app.register_blueprint(portfolio_bp, url_prefix='/portfolios')
        app.register_blueprint(security_bp, url_prefix='/securities')
        app.register_blueprint(trade_bp, url_prefix='/trades')

        return app
    except Exception as e:
        print(f'Error creating app: {e}')
        raise
