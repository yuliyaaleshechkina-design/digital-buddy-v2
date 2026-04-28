from flask import Blueprint, request, jsonify
from utils.database import add_alert, get_active_alerts, resolve_alert

bp = Blueprint('alerts', __name__)

@bp.route('/add-alert/<newcomer_id>', methods=['POST'])
def add_alert_route(newcomer_id):
    data = request.json
    level = data.get('level', 'medium')
    reason = data.get('reason')
    
    if not reason:
        return jsonify({'error': 'Reason required'}), 400
    
    add_alert(newcomer_id, level, reason)
    return jsonify({'success': True})

@bp.route('/get-active-alerts', methods=['GET'])
def get_active_alerts_route():
    alerts = get_active_alerts()
    return jsonify(alerts)

@bp.route('/resolve-alert/<alert_id>', methods=['POST'])
def resolve_alert_route(alert_id):
    resolve_alert(alert_id)
    return jsonify({'success': True})

@bp.route('/get-dashboard-summary', methods=['GET'])
def get_dashboard_summary_route():
    from utils.database import get_dashboard_summary
    summary = get_dashboard_summary()
    return jsonify(summary)
