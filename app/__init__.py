from flask import Flask, jsonify
from flask_caching import Cache
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from app.config import get_config
from app.db import db
from app.routes import portfolio_bp, security_bp, trade_bp, user_bp
from app.schemas import ErrorResponse

cache = Cache()


from flask_cors import CORS

def create_app(config_name=None):
    try:
        app = Flask(__name__)
        config = get_config(config_name)
        app.config.from_object(config)

        # register extensions
        db.init_app(app)
        cache.init_app(app)
        CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
        app.cache = cache

        # register blueprints
        app.register_blueprint(user_bp, url_prefix='/users')
        app.register_blueprint(portfolio_bp, url_prefix='/portfolios')
        app.register_blueprint(security_bp, url_prefix='/securities')
        app.register_blueprint(trade_bp, url_prefix='/trades')

        # register error handlers
        @app.errorhandler(HTTPException)
        def handle_http_exception(e):
            return jsonify(ErrorResponse(error=e.name, detail=e.description).model_dump()), e.code

        @app.errorhandler(Exception)
        def handle_exception(e):
            db.session.rollback()
            return jsonify(ErrorResponse(error='An internal error occurred', detail=str(e)).model_dump()), 500

        @app.errorhandler(ValidationError)
        def handle_validation_error(e):
            return jsonify(ErrorResponse(error='Validation error', detail=str(e.errors())).model_dump()), 422

        return app
    except Exception as e:
        print(f'Error creating app: {e}')
        raise
