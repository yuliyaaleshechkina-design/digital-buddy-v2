from flask import Blueprint, request, jsonify
from utils.database import (
    create_session, get_messages, add_message,
    get_tasks, add_task_comment, get_task_comments, update_task_status
)
from models.ai import generate_bot_response, analyze_sentiment, check_alert_triggers
from datetime import datetime

bp = Blueprint('chat', __name__)

@bp.route('/start-session/<newcomer_id>', methods=['POST'])
def start_session_route(newcomer_id):
    token = create_session(newcomer_id)
    return jsonify({'success': True, 'token': token})

@bp.route('/get-messages/<newcomer_id>', methods=['GET'])
def get_messages_route(newcomer_id):
    messages = get_messages(newcomer_id)
    return jsonify(messages)

@bp.route('/send-message/<newcomer_id>', methods=['POST'])
def send_message_route(newcomer_id):
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    add_message(newcomer_id, message, 'user')
    sentiment, confidence = analyze_sentiment(message)
    triggers = check_alert_triggers(message)
    
    from utils.database import get_newcomer
    newcomer_data = get_newcomer(newcomer_id)
    newcomer_name = newcomer_data['name'] if newcomer_data else 'Новичок'
    
    bot_response = generate_bot_response(message, newcomer_name)
    add_message(newcomer_id, bot_response, 'buddy')
    
    system_messages = []
    if triggers:
        for trigger in triggers:
            add_message(newcomer_id, f"[Система: {trigger}]", 'system')
            system_messages.append(trigger)
    
    return jsonify({
        'success': True,
        'bot_response': bot_response,
        'sentiment': sentiment,
        'triggers': system_messages
    })

@bp.route('/get-tasks/<newcomer_id>', methods=['GET'])
def get_tasks_route(newcomer_id):
    tasks = get_tasks(newcomer_id)
    return jsonify(tasks)

@bp.route('/add-task-comment/<task_id>', methods=['POST'])
def add_task_comment_route(task_id):
    data = request.json
    newcomer_id = data.get('newcomer_id')
    comment = data.get('comment')
    
    if not comment or not newcomer_id:
        return jsonify({'error': 'Missing fields'}), 400
    
    add_task_comment(task_id, newcomer_id, comment)
    return jsonify({'success': True})

@bp.route('/update-task-status/<task_id>', methods=['POST'])
def update_task_status_route(task_id):
    data = request.json
    status = data.get('status')
    
    if not status:
        return jsonify({'error': 'Status required'}), 400
    
    update_task_status(task_id, status)
    return jsonify({'success': True})
