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
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        db.drop_all()

    # helper functions

    """Viewer helper function"""
    def create_viewer(self, email):
        return self.app.post('/viewer', json={'email': email})

    """Meeting helper function"""
    def create_meeting(self, host_email, password):
        return self.app.post('/meeting', json={'host_email': host_email, 'password': password})

    """Recording helper function"""
    def create_recording(self, url, is_private, meeting_id):
        return self.app.post('/recording', json={'url': url, 'is_private': is_private, 'meeting_id': meeting_id})

    def delete_recording(self, url):
        return self.app.get('/recording/delete/' + url)

    # assert functions
    def test_empty_meeting(self):
        """Ensure meeting list is empty"""
        all_meetings = models.Meeting.query.all()
        self.assertEqual([], all_meetings)

    def test_create_new_meeting(self):
        """Ensure that the meeting is created"""
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        meeting = models.Meeting.query.get(1)
        self.assertEqual(email, meeting.host_email)
        self.assertEqual(password, meeting.password)

    def test_invalid_host_email(self):
        """Ensure the host email is from a valid viewer"""
        host_email = "invalid@email.com"
        password = "pass"
        rv = self.create_meeting(host_email, password)
        json_data = rv.get_json()
        self.assertEqual("Invalid host email.", json_data['message'])

    def test_create_new_recording(self):
        """Ensure that a new recording is created"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = False
        meeting_id = 1
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        recording = models.Recording.query.get(url)
        self.assertEqual(url, recording.url)
        self.assertEqual(is_private, recording.is_private)
        self.assertEqual(meeting_id, recording.meeting_id)

    def test_delete_recording(self):
        """Ensure that a new recording is created"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = False
        meeting_id = 1
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        self.delete_recording(url)
        recordings = models.Recording.query.all()
        self.assertEqual([], recordings)

    def test_url_already_exists(self):
        """Ensure the url from a recording is unique"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = False
        meeting_id = 1
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        rv = self.create_recording(url, is_private, meeting_id)
        json_data = rv.get_json()
        self.assertEqual("URL already exists.", json_data['message'])

    def test_invalid_meeting_id(self):
        """Ensure the meeting id from a recording is valid"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = False
        meeting_id = 100
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        rv = self.create_recording(url, is_private, meeting_id)
        json_data = rv.get_json()
        self.assertEqual("Invalid meeting id.", json_data['message'])


if __name__ == '__main__':
    unittest.main()
