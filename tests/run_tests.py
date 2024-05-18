import unittest
from app import create_app, db
from app.models import Users
from flask import url_for
from app.config import TestingConfig  # Import TestingConfig

class BasicTests(unittest.TestCase):

    def setUp(self):
        """Set up the test client and initialize the database."""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down the database and application context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """Test that the home page loads correctly."""
        with self.app.test_request_context():
            response = self.client.get(url_for('main.home'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Home', response.data)

    def test_login_page(self):
        """Test that the login page loads correctly."""
        with self.app.test_request_context():
            response = self.client.get(url_for('main.login'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login', response.data)

    def test_create_account(self):
        """Test account creation."""
        with self.app.test_request_context():
            response = self.client.post(url_for('main.create_account'), data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpassword'
            }, follow_redirects=True)  # Follow redirects to handle flashes
            self.assertEqual(response.status_code, 200)
            user = Users.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'test@example.com')

if __name__ == '__main__':
    unittest.main()
