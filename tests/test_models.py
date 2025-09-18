import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Task, Category
from config import TestConfig


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='testuser')
        u.set_password('password123')
        self.assertFalse(u.check_password('wrongpassword'))
        self.assertTrue(u.check_password('password123'))

    def test_user_creation(self):
        u = User(username='testuser', email='test@example.com')
        db.session.add(u)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(u.username, 'testuser')

    def test_task_creation(self):
        u = User(username='testuser', email='test@example.com')
        db.session.add(u)
        db.session.commit()
        
        t = Task(title='Test Task', description='Test Description', author=u)
        db.session.add(t)
        db.session.commit()
        
        self.assertEqual(Task.query.count(), 1)
        self.assertEqual(t.title, 'Test Task')
        self.assertEqual(t.author, u)
        self.assertFalse(t.completed)

    def test_category_creation(self):
        c = Category(name='Work', description='Work related tasks')
        db.session.add(c)
        db.session.commit()
        
        self.assertEqual(Category.query.count(), 1)
        self.assertEqual(c.name, 'Work')

    def test_task_to_dict(self):
        u = User(username='testuser', email='test@example.com')
        c = Category(name='Work')
        db.session.add(u)
        db.session.add(c)
        db.session.commit()
        
        t = Task(title='Test Task', description='Test Description', 
                author=u, category=c, priority='high')
        db.session.add(t)
        db.session.commit()
        
        task_dict = t.to_dict()
        self.assertEqual(task_dict['title'], 'Test Task')
        self.assertEqual(task_dict['category'], 'Work')
        self.assertEqual(task_dict['priority'], 'high')
        self.assertFalse(task_dict['completed'])


if __name__ == '__main__':
    unittest.main()