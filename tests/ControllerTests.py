import unittest
from unittest.mock import patch
from app import create_app, db
from app.models import Users, Polls, VotePoll, Comments
from flask import flash
from app.config import TestingConfig
from app.Controller import *

class ControllerTests(unittest.TestCase):
    def setUp(self):
        """Set up the test client and initialize the database."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        test_data()
        
    def tearDown(self):
        """Tear down the database and application context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_valid_login(self):
            users = Users.query.all()

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

    def test_valid_password(self):
            self.assertFalse(valid_password("Something11"))
            self.assertFalse(valid_password("password-c"))
            self.assertFalse(valid_password("Password-a"))
            self.assertFalse(valid_password("something-11"))
            self.assertTrue(valid_password("Some-thing11"))
            self.assertTrue(valid_password("Password-thing99"))
            self.assertTrue(valid_password("cool-Password99"))


    def test_unique_username(self):
            self.assertFalse(unique_username("user1"))
            self.assertFalse(unique_username("user23"))
            self.assertFalse(unique_username("user99"))
            self.assertTrue(unique_username("Cool_username99"))
            self.assertTrue(unique_username("MagMicro"))
            self.assertTrue(unique_username("Jamie99"))
            self.assertTrue(unique_username("jeremy66"))

    def test_unique_email(self):
            self.assertFalse(unique_email("someone1@email.com"))
            self.assertFalse(unique_email("someone22@email.com"))
            self.assertFalse(unique_email("someone93@email.com"))
            self.assertTrue(unique_email("someone101@gmail.com"))
            self.assertTrue(unique_email("username@gmail.com"))
            self.assertTrue(unique_email("user232@gmail.com"))

    def test_register_account(self):
        register_account("MagMicro", "someone101@gmail.com", "cool-Password99")
        register_account("Jamie99", "username@gmail.com", "Password-thing99")
        register_account("jeremy66", "user232@gmail.com", "cool-Password99")
        self.assertIsNotNone(Users.query.filter_by(username = "MagMicro").first())
        self.assertIsNotNone(Users.query.filter_by(username = "Jamie99").first())
        self.assertIsNotNone(Users.query.filter_by(email = "user232@gmail.com").first())

        self.assertIsNone(Users.query.filter_by(username = "MagMicro11").first())
        self.assertIsNone(Users.query.filter_by(username = "Jamie2001").first())
        self.assertIsNone(Users.query.filter_by(email = "user111@gmail.com").first())

    def test_create_poll(self):
        create_poll("cat", "dog", 1, "Better Pet?", ["Animals"])
        create_poll("red", "blue", 84, "Better colour?", ["Colour", "Horror", "Comedy"])
        create_poll("c#", "java", 23, "Better language?", ["Programming", "Sci-Fi"])

        self.assertIsNotNone(Polls.query.filter_by(prompt = "Better colour?").first())
        self.assertIsNotNone(Polls.query.filter_by(user_ID = 1, Option1 = "cat").first())
        self.assertIsNotNone(Polls.query.filter_by(tag1 = "Programming").first())
        self.assertIsNotNone(Polls.query.filter_by(tag1 = "Animals" , Option1 = "cat", Option2 = "dog", user_ID = 1, prompt = "Better Pet?").first())

        self.assertIsNone(Polls.query.filter_by(user_ID = 88).first())
