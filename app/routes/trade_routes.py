from flask import Blueprint, g, jsonify, request

from app.auth.auth import require_auth
from app.db import db
from app.schemas import BuyTradeRequest, SellTradeRequest
from app.service import trade_service
from app.service.portfolio_access_service import check_access

trade_bp = Blueprint('trade', __name__)


@trade_bp.route('/buy', methods=['POST'])
@require_auth
def execute_purchase_order():
    req_data = BuyTradeRequest(**request.get_json())
    if not check_access(req_data.portfolio_id, g.user_id, 'manager'):
        return jsonify({'error': 'Forbidden'}), 403
    trade_service.execute_purchase_order(
        portfolio_id=req_data.portfolio_id,
        ticker=req_data.ticker,
        quantity=req_data.quantity,
    )
    db.session.commit()
    return jsonify({'message': 'Purchase order executed successfully'}), 201


@trade_bp.route('/sell', methods=['POST'])
@require_auth
def liquidate_investment():
    req_data = SellTradeRequest(**request.get_json())
    if not check_access(req_data.portfolio_id, g.user_id, 'manager'):
        return jsonify({'error': 'Forbidden'}), 403
    trade_service.liquidate_investment(
        portfolio_id=req_data.portfolio_id,
        ticker=req_data.ticker,
        quantity=req_data.quantity,
    )
    db.session.commit()
    return jsonify({'message': 'Investment liquidated successfully'}), 200
