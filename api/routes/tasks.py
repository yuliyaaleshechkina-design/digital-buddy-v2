from flask import Blueprint, request, jsonify
from utils.database import (
    add_task, get_tasks, update_task_status, 
    add_task_comment, get_task_comments, 
    get_all_tasks_for_hr, create_initial_tasks, delete_task, get_task
)

bp = Blueprint('tasks', __name__)

@bp.route('/add-task/<newcomer_id>', methods=['POST'])
def add_task_route(newcomer_id):
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    deadline = data.get('deadline', '')
    
    if not title:
        return jsonify({'error': 'Title required'}), 400
    
    task_id = add_task(newcomer_id, title, description, deadline)
    return jsonify({'success': True, 'task_id': task_id})

@bp.route('/get-tasks/<newcomer_id>', methods=['GET'])
def get_tasks_route(newcomer_id):
    tasks = get_tasks(newcomer_id)
    return jsonify(tasks)

@bp.route('/update-task-status/<task_id>', methods=['POST'])
def update_task_status_route(task_id):
    data = request.json
    status = data.get('status')
    
    if not status:
        return jsonify({'error': 'Status required'}), 400
    
    update_task_status(task_id, status)
    return jsonify({'success': True})

@bp.route('/add-comment/<task_id>', methods=['POST'])
def add_comment_route(task_id):
    data = request.json
    newcomer_id = data.get('newcomer_id')
    comment = data.get('comment')
    
    if not comment or not newcomer_id:
        return jsonify({'error': 'Missing fields'}), 400
    
    add_task_comment(task_id, newcomer_id, comment)
    return jsonify({'success': True})

@bp.route('/get-comments/<task_id>', methods=['GET'])
def get_comments_route(task_id):
    comments = get_task_comments(task_id)
    return jsonify(comments)

@bp.route('/get-all-tasks', methods=['GET'])
def get_all_tasks_route():
    tasks = get_all_tasks_for_hr()
    return jsonify(tasks)

@bp.route('/create-initial-tasks/<newcomer_id>', methods=['POST'])
def create_initial_tasks_route(newcomer_id):
    task_ids = create_initial_tasks(newcomer_id)
    return jsonify({'success': True, 'task_ids': task_ids})

@bp.route('/delete-task/<task_id>', methods=['POST'])
def delete_task_route(task_id):
    delete_task(task_id)
    return jsonify({'success': True})

@bp.route('/get-task/<task_id>', methods=['GET'])
def get_task_route(task_id):
    task = get_task(task_id)
    if task:
        return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404
