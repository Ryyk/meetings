import unittest
import os
import json

from app import app, db
import models

TEST_DB = 'test.db'

class MeetingsApiTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a blank temp database befor each test"""
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        db.drop_all()

    def test_empty_meeting(self):
        """Ensure meeting list is empty"""
        all_meetings = models.Meeting.query.all()
        self.assertEqual([], all_meetings)
    
    def test_create_meeting(self):
        email = "test@email.com"
        password = "password"
        # inserting viewer db
        new_viewer = models.Viewer(email)
        db.session.add(new_viewer)
        db.session.commit()
        rv = self.app.post('/meeting', json={
            'host_email': email, 'password': password
        })
        json_data = rv.get_json()

        self.assertEqual(email, json_data['host_email'])
        self.assertEqual(password, json_data['password'])

    def test_invalid_host_email(self):
        """Ensure the host email is from a valid viewer"""
        host_email = "invalid@email.com"
        password = "password"
        rv = self.app.post('/meeting', json={
            'host_email': host_email, 'password': password
        })
        json_data = rv.get_json()
        self.assertEqual("Invalid host email.", json_data['message'])



if __name__ == '__main__':
    unittest.main()