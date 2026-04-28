from flask import Blueprint, request, jsonify
from utils.database import add_mood_checkin, get_mood_history, get_all_mood_checkins

bp = Blueprint('mood', __name__)

@bp.route('/add-mood/<newcomer_id>', methods=['POST'])
def add_mood_route(newcomer_id):
    data = request.json
    mood_score = data.get('mood_score')
    feedback = data.get('feedback', '')
    
    if not mood_score:
        return jsonify({'error': 'Mood score required'}), 400
    
    add_mood_checkin(newcomer_id, mood_score, feedback)
    return jsonify({'success': True})

@bp.route('/get-mood-history/<newcomer_id>', methods=['GET'])
def get_mood_history_route(newcomer_id):
    days = request.args.get('days', 30, type=int)
    history = get_mood_history(newcomer_id, days)
    return jsonify(history)

@bp.route('/get-all-mood', methods=['GET'])
def get_all_mood_route():
    mood_data = get_all_mood_checkins()
    return jsonify(mood_data)
