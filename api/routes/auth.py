from flask import Blueprint, request, jsonify
from utils.database import add_newcomer, get_newcomer, get_all_newcomers

bp = Blueprint('auth', __name__)

@bp.route('/add-newcomer', methods=['POST'])
def add_newcomer_route():
    data = request.json
    name = data.get('name')
    position = data.get('position')
    department = data.get('department')
    start_date = data.get('start_date')
    mentor_name = data.get('mentor_name', '')
    
    if not all([name, position, department, start_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    newcomer_id = add_newcomer(name, position, department, start_date, mentor_name)
    
    if newcomer_id:
        return jsonify({'success': True, 'newcomer_id': newcomer_id})
    else:
        return jsonify({'error': 'Newcomer already exists'}), 400

@bp.route('/get-newcomer/<newcomer_id>', methods=['GET'])
def get_newcomer_route(newcomer_id):
    newcomer = get_newcomer(newcomer_id)
    if newcomer:
        return jsonify(newcomer)
    else:
        return jsonify({'error': 'Newcomer not found'}), 404

@bp.route('/get-all-newcomers', methods=['GET'])
def get_all_newcomers_route():
    newcomers = get_all_newcomers()
    return jsonify(newcomers)
