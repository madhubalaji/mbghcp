import unittest
from app import create_app, db
from app.models import User, Task, Category
from config import TestConfig


class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_redirect_when_not_logged_in(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_login_page(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)

    def test_register_page(self):
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_user_registration(self):
        response = self.client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.query.count(), 1)

    def test_user_login(self):
        # Create a user first
        u = User(username='testuser', email='test@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        # Test login
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_api_tasks_unauthorized(self):
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def login_user(self):
        """Helper method to log in a user for testing"""
        u = User(username='testuser', email='test@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()
        
        self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        return u

    def test_api_tasks_authorized(self):
        user = self.login_user()
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_task_via_api(self):
        user = self.login_user()
        response = self.client.post('/api/tasks', 
                                  json={'title': 'Test Task', 'description': 'Test Description'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.query.count(), 1)


if __name__ == '__main__':
    unittest.main()