#!/usr/bin/env python3
"""
Development server runner for Task Manager application.
"""

from app import create_app, db
from app.models import User, Task, Category

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Task': Task, 
        'Category': Category
    }


@app.cli.command()
def init_db():
    """Initialize the database with sample data."""
    db.create_all()
    
    # Create sample categories
    if Category.query.count() == 0:
        categories = [
            Category(name='Work', description='Work related tasks', color='#007bff'),
            Category(name='Personal', description='Personal tasks', color='#28a745'),
            Category(name='Shopping', description='Shopping list items', color='#ffc107'),
            Category(name='Health', description='Health and fitness tasks', color='#dc3545'),
        ]
        
        for category in categories:
            db.session.add(category)
    
    # Create sample admin user
    if User.query.filter_by(username='admin').first() is None:
        admin = User(username='admin', email='admin@taskmanager.com')
        admin.set_password('admin123')
        db.session.add(admin)
    
    db.session.commit()
    print('Database initialized with sample data!')


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)