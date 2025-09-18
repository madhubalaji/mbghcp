from flask import jsonify, request
from flask_login import login_required, current_user
from app import db
from app.api import bp
from app.models import Task, Category


@bp.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    """Get all tasks for the current user"""
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([task.to_dict() for task in tasks])


@bp.route('/tasks/<int:id>', methods=['GET'])
@login_required
def get_task(id):
    """Get a specific task"""
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return jsonify(task.to_dict())


@bp.route('/tasks', methods=['POST'])
@login_required
def create_task():
    """Create a new task"""
    data = request.get_json() or {}
    
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        user_id=current_user.id
    )
    
    if 'category_id' in data:
        task.category_id = data['category_id']
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201


@bp.route('/tasks/<int:id>', methods=['PUT'])
@login_required
def update_task(id):
    """Update a task"""
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    if 'priority' in data:
        task.priority = data['priority']
    if 'category_id' in data:
        task.category_id = data['category_id']
    
    db.session.commit()
    return jsonify(task.to_dict())


@bp.route('/tasks/<int:id>', methods=['DELETE'])
@login_required
def delete_task(id):
    """Delete a task"""
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return '', 204


@bp.route('/categories', methods=['GET'])
@login_required
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'description': cat.description,
        'color': cat.color
    } for cat in categories])