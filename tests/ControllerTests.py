import unittest
from app import create_app, db
from app.models import Users, Polls, VotePoll, Comments
from flask import url_for
from app.config import TestingConfig
from app.Controller import *

def test_data():
      for i in range(100):
            username = "user" + str(i)
            password = "Some-thing1" + str(i)
            email = "someone" + str(i) + "@email.com"
            user = Users(username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit(user)

class ControllerTests(unittest.TestCase):
    def setUp(self):
        """Set up the test client and initialize the database."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.init_app(self.app)
        db.create_all()
        test_data()
        
    def tearDown(self):
        """Tear down the database and application context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

def test_valid_login(self):
        users = Users.query.all()

        # Checks if all logins are valid
        for user in users:
                self.assertTrue(valid_login(user.username, user.password))

                # Case user doesnt exist
                self.assertFalse(valid_login("Somebody11", "randompassword"))
                self.assertFalse(valid_login("random11", "PASS-word11"))
                self.assertFalse(valid_login("user101", "Some-thing1101"))

                # Case user exists, but wrong password
                self.assertFalse(valid_login("user5", "some_random_PASSWORD11"))
                self.assertFalse(valid_login("user9","Something-17"))
                self.assertFalse(valid_login("user27","Something-128"))

                # Case the the user does exist
                self.assertTrue(valid_login("user5", "Some-thing15"))
                self.assertTrue(valid_login("user9","Some-thing19"))
                self.assertTrue(valid_login("user27","Some-thing127"))