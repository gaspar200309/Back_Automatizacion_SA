import unittest
from app import create_app, db
from app.models import User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        response = self.app.test_client().post('/register', json=dict(username='testuser', password='password'))
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_login_user(self):
        self.app.test_client().post('/register', json=dict(username='testuser', password='password'))
        response = self.app.test_client().post('/login', json=dict(username='testuser', password='password'))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
