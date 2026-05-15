from flask import Blueprint, g, jsonify, request

import app.service.portfolio_service as portfolio_service
import app.service.transaction_service as transaction_service
import app.service.user_service as user_service
from app.auth.auth import require_auth
from app.db import db
from app.schemas import CreatePortfolioRequest, GrantAccessRequest
from app.service.portfolio_access_service import check_access

portfolio_bp = Blueprint('portfolio', __name__)


@portfolio_bp.route('/', methods=['GET'])
@require_auth
def get_all_portfolios():
    portfolios = portfolio_service.get_all_portfolios()
    return jsonify([portfolio.__to_dict__() for portfolio in portfolios]), 200


@portfolio_bp.route('/<int:portfolio_id>', methods=['GET'])
@require_auth
def get_portfolio(portfolio_id):
    if not check_access(portfolio_id, g.user_id):
        return jsonify({'error': 'Forbidden'}), 403
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
    if portfolio is None:
        return jsonify({'error': f'Portfolio {portfolio_id} not found'}), 404
    return jsonify(portfolio.__to_dict__()), 200


@portfolio_bp.route('/user/<username>', methods=['GET'])
@require_auth
def get_portfolios_by_user(username):
    user = user_service.get_user_by_username(username)
    if user is None:
        return jsonify({'error': f'User {username} not found'}), 404
    portfolios = portfolio_service.get_portfolios_by_user(user)
    return jsonify([portfolio.__to_dict__() for portfolio in portfolios]), 200


@portfolio_bp.route('/', methods=['POST'])
@require_auth
def create_portfolio():
    req_data = CreatePortfolioRequest(**request.get_json())
    if g.user_id != req_data.username:
        return jsonify({'error': 'Forbidden'}), 403
    user = user_service.get_user_by_username(req_data.username)
    if user is None:
        return jsonify({'error': f'User {req_data.username} not found'}), 404
    portfolio = portfolio_service.create_portfolio(
        name=req_data.name,
        description=req_data.description,
        user=user,
    )
    db.session.commit()
    return jsonify({'message': 'Portfolio created successfully', 'portfolio_id': portfolio.id}), 201


@portfolio_bp.route('/<int:portfolio_id>', methods=['DELETE'])
@require_auth
def delete_portfolio(portfolio_id):
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
    if not portfolio or portfolio.owner != g.user_id:
        return jsonify({'error': 'Forbidden'}), 403
    portfolio_service.delete_portfolio(portfolio_id)
    db.session.commit()
    return jsonify({'message': 'Portfolio deleted successfully'}), 200


@portfolio_bp.route('/<int:portfolio_id>/access', methods=['POST'])
@require_auth
def grant_portfolio_access(portfolio_id):
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
    if not portfolio or portfolio.owner != g.user_id:
        return jsonify({'error': 'Forbidden'}), 403
    req_data = GrantAccessRequest(**request.get_json())
    from app.service.portfolio_access_service import grant_access
    grant_access(portfolio_id, req_data.user_id, req_data.role)
    db.session.commit()
    return jsonify({'message': 'Access granted'}), 201


@portfolio_bp.route('/<int:portfolio_id>/access/<user_id>', methods=['DELETE'])
@require_auth
def revoke_portfolio_access(portfolio_id, user_id):
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
    if not portfolio or portfolio.owner != g.user_id:
        return jsonify({'error': 'Forbidden'}), 403
    from app.service.portfolio_access_service import revoke_access
    revoke_access(portfolio_id, user_id)
    db.session.commit()
    return jsonify({'message': 'Access revoked'}), 200

@portfolio_bp.route('/me', methods=['GET'])
@require_auth
def get_my_portfolios():
    user = user_service.get_user_by_username(g.user_id)
    if user is None:
        return jsonify([]), 200
    portfolios = portfolio_service.get_portfolios_by_user(user)
    return jsonify([portfolio.__to_dict__() for portfolio in portfolios]), 200

@portfolio_bp.route('/<int:portfolio_id>/holdings', methods=['GET'])
@require_auth
def get_portfolio_holdings(portfolio_id):
    if not check_access(portfolio_id, g.user_id):
        return jsonify({'error': 'Forbidden'}), 403
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
    if portfolio is None:
        return jsonify({'error': f'Portfolio {portfolio_id} not found'}), 404
    holdings = portfolio_service.get_holdings(portfolio_id)
    return jsonify([h.__to_dict__() for h in holdings]), 200

@portfolio_bp.route('/<int:portfolio_id>/transactions', methods=['GET'])
@require_auth
def get_portfolio_transactions(portfolio_id):
    if not check_access(portfolio_id, g.user_id):
        return jsonify({'error': 'Forbidden'}), 403
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
    if portfolio is None:
        return jsonify({'error': f'Portfolio {portfolio_id} not found'}), 404
    transactions = transaction_service.get_transactions_by_portfolio_id(portfolio_id)
    transactions.sort(key=lambda t: t.date_time, reverse=True)
    return jsonify([t.__to_dict__() for t in transactions]), 200
