import unittest
from app import create_app, db
from app.models import Users, Polls, VotePoll
from flask import url_for
from app.config import TestingConfig

class BasicTests(unittest.TestCase):

    def setUp(self):
        """Set up the test client and initialize the database."""
        self.app = create_app(TestingConfig)
        self.app.config['SERVER_NAME'] = 'localhost'
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
        with self.client:
            response = self.client.get(url_for('main.home'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Home', response.data)

    def test_login_page(self):
        """Test that the login page loads correctly."""
        with self.client:
            response = self.client.get(url_for('main.login'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login', response.data)

    def test_register_user_with_invalid_password(self):
        """Test user registration with missing or invalid data."""
        with self.client:
            response = self.client.post(url_for('main.create_account'), data={
                'username': 'testuser',
                'email': 'em@mail.com',
                'password': 'password'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            assert(Users.query.all() == [])

    def test_register_user_with_invalid_email(self):
        """Test user registration with missing or invalid data."""
        with self.client:
            response = self.client.post(url_for('main.create_account'), data={
                'username': 'testuser',
                'email': 'email',
                'password': 'Password12345!'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            assert(Users.query.all() == [])

    def test_make_poll(self):
        """Test poll creation."""
        with self.client:
            # Create a test user account
            response = self.client.post(url_for('main.create_account'), data={
                'username': 'testuser',
                'email': 'tests@example.com',
                'password': 'Password12345!'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            # Verify the user was created
            user = Users.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            
            # Log the test user in
            response = self.client.post(url_for('main.login'), data={
                'username': 'testuser', 
                'password': 'Password12345!'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            # Ensure the user is logged in
            with self.client.session_transaction() as sess:
                self.assertTrue('_user_id' in sess)
            
            # Define the poll data
            prompt = 'Test poll'
            option1 = 'Option 1'
            option2 = 'Option 2'
            form_tags = 'Sports'

            # Create the poll
            response = self.client.post(url_for('main.create'), data={
                'prompt': prompt,
                'option1': option1,
                'option2': option2,
                'tags': form_tags  # Ensure the field name matches your form
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)            

            # Check for flash messages
            with self.client.session_transaction() as sess:
                flash_messages = sess.get('_flashes', [])
                print(flash_messages)
            
            # Verify the poll was created
            poll = Polls.query.filter_by(prompt=prompt).first()
            self.assertIsNotNone(poll)

    def test_vote_poll(self):
        """Test poll creation."""
        with self.client:
            # Create a test user account
            response = self.client.post(url_for('main.create_account'), data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'Password12345!'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            # Verify the user was created
            user = Users.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            
            # Log the test user in
            response = self.client.post(url_for('main.login'), data={
                'username': 'testuser',  # Use username if that's how your form identifies
                'password': 'Password12345!'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            # Ensure the user is logged in
            with self.client.session_transaction() as sess:
                self.assertTrue('_user_id' in sess)
            
            # Define the poll data
            prompt = 'Test poll'
            option1 = 'Option 1'
            option2 = 'Option 2'
            form_tags = 'Sports'

            # Create the poll
            response = self.client.post(url_for('main.create'), data={
                'prompt': prompt,
                'option1': option1,
                'option2': option2,
                'tags': form_tags  # Ensure the field name matches your form
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)            

            # Check for flash messages
            with self.client.session_transaction() as sess:
                flash_messages = sess.get('_flashes', [])
                print(flash_messages)
            
            # Verify the poll was created
            poll = Polls.query.filter_by(prompt=prompt).first()
            self.assertIsNotNone(poll)

            # Make a second account to vote on the poll
            response = self.client.post(url_for('main.create_account'), data={
                'username': 'testuser2',
                'email': 'test2@mail.com',
                'password': 'Password12345!'
            }, follow_redirects=True)

            # Verify the user was created
            user = Users.query.filter_by(username='testuser2').first()
            self.assertIsNotNone(user)

            # Log the test user in
            response = self.client.post(url_for('main.login'), data={
                'username': 'testuser2',
                'password': 'Password12345!'
            }, follow_redirects=True)

            # Ensure the user is logged in
            with self.client.session_transaction() as sess:
                self.assertTrue('_user_id' in sess)

            # Vote on the poll
            response = self.client.post(url_for('main.cast_vote'), data={
                'poll_ID': '1',
                'user_ID': '2', 
                'option': 'option1'
            }, follow_redirects=True)

            # Check for flash messages
            with self.client.session_transaction() as sess:
                flash_messages = sess.get('_flashes', [])
                print(flash_messages)

            # Verify the vote was recorded
            vote = VotePoll.query.all()
            self.assertIsNotNone(vote)
           
if __name__ == '__main__':
    unittest.main()
