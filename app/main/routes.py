from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import TaskForm, CategoryForm
from app.models import Task, Category


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    filter_status = request.args.get('status', 'all')
    filter_category = request.args.get('category', 'all')
    
    query = current_user.tasks
    
    if filter_status == 'completed':
        query = query.filter_by(completed=True)
    elif filter_status == 'pending':
        query = query.filter_by(completed=False)
    
    if filter_category != 'all':
        query = query.filter_by(category_id=filter_category)
    
    tasks = query.order_by(Task.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    categories = Category.query.all()
    
    return render_template('index.html', title='Dashboard', tasks=tasks, 
                         categories=categories, filter_status=filter_status,
                         filter_category=filter_category)


@bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    form.category.choices.insert(0, (0, 'No Category'))
    
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            category_id=form.category.data if form.category.data != 0 else None,
            author=current_user
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('add_task.html', title='Add Task', form=form)


@bp.route('/edit_task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    form.category.choices.insert(0, (0, 'No Category'))
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.category_id = form.category.data if form.category.data != 0 else None
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('edit_task.html', title='Edit Task', form=form, task=task)


@bp.route('/delete_task/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.index'))


@bp.route('/toggle_task/<int:id>')
@login_required
def toggle_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'status': 'success', 'completed': task.completed})


@bp.route('/categories')
@login_required
def categories():
    categories = Category.query.all()
    return render_template('categories.html', title='Categories', categories=categories)


@bp.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data,
            color=form.color.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('main.categories'))
    
    return render_template('add_category.html', title='Add Category', form=form)