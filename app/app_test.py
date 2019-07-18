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
        return self.app.post('/viewer/create', json={'email': email})

    """Meeting helper function"""
    def create_meeting(self, host_email, password):
        return self.app.post('/meeting/create', json={'host_email': host_email, 'password': password})

    """Recording helper function"""
    def create_recording(self, url, is_private, meeting_id):
        return self.app.post('/recording/create', json={'url': url, 'is_private': is_private, 'meeting_id': meeting_id})

    def delete_recording(self, url):
        return self.app.post('/recording/delete', json={'url': url})

    def share_recording(self, email, url):
        return self.app.post('/recording/share', json={'url': url, "email": email})

    def has_access_recording(self, email, url, password):
        return self.app.get('/recording/has-access', json={'email': email, "url": url, "password": password})

    # assert functions
    def test_empty_meeting(self):
        """Ensure meeting list is empty"""
        all_meetings = models.Meeting.query.all()
        self.assertEqual([], all_meetings)


    # "/meeting/create" tests

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

    # "/viewers/create" tests

    def test_create_new_viewer(self):
        """Ensure that the viewer is created"""
        email = "test@email.com"
        self.create_viewer(email)
        viewer = models.Viewer.query.get(1)
        self.assertEqual(email, viewer.email)

    def test_invalid_email_syntax(self):
        """Ensure that the viewer email is valid"""
        email = "test@"
        rv = self.create_viewer(email)
        json_data = rv.get_json()
        self.assertEqual("Invalid email.", json_data['message'])

    def test_duplicated_email(self):
        """Ensure that the viewer email is unique"""
        email = "test@email.com"
        self.create_viewer(email)
        rv = self.create_viewer(email)
        json_data = rv.get_json()
        self.assertEqual("Email already in use.", json_data['message'])

    # "/recording/create" tests

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

    # "/recording/delete" tests

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

    def test_invalid_url_delete_recording(self):
        """Ensure that the URL given is valid"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = False
        meeting_id = 1
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        rv = self.delete_recording("https://invalid.url")
        json_data = rv.get_json()
        self.assertEqual("URL does not exist.", json_data['message'])

    # "/recording/share" tests

    def test_share_recording(self):
        """Ensure that the recording is shared"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = False
        meeting_id = 1
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        self.share_recording(email, url)

        viewers = models.Recording.query.get(url).viewers
        self.assertEqual(email, viewers[0].email)

    def test_email_without_match_share_recording(self):
        """Ensure that the email given is valid when sharing a recording"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = False
        meeting_id = 1
        email = "test@email.com"
        invalid_email = "invalid@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        rv = self.share_recording(invalid_email, url)
        json_data = rv.get_json()
        message = "The Email " + invalid_email + " does not belong to a valid viewer."
        self.assertEqual(message, json_data['message'])

    def test_invalid_url_share_recording(self):
        """Ensure that the url given is valid when sharing a recording"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        invalid_url = "https://s3.amazonaws.com/meetings/invalid/"
        is_private = False
        meeting_id = 1
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        rv = self.share_recording(email, invalid_url)
        json_data = rv.get_json()
        message = "The URL " + invalid_url + " does not belong to a valid Recording."
        self.assertEqual(message, json_data['message'])

    def test_duplicated_viewer_share_recording(self):
        """Ensure that there are no duplicated viewers when sharing a recording"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = False
        meeting_id = 1
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        self.share_recording(email, url)
        rv = self.share_recording(email, url)
        json_data = rv.get_json()
        message = "Cannot share meeting:" + url + " with the viewer " + email + " twice."
        self.assertEqual(message, json_data['message'])

    def test_add_viewer_private_recording_share(self):
        """Ensure that it is not possible to add viewers to private recordings"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = True
        meeting_id = 1
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        rv = self.share_recording(email, url)
        json_data = rv.get_json()
        message = "Cannot add viewers to a private Recording."
        self.assertEqual(message, json_data['message'])

    # "/recording/has-access" tests

    def test_email_without_match(self):
        """Ensure the email has a viewer associated"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        password = "pass"
        rv = self.has_access_recording("invalid@email.com", url, password)
        json_data = rv.get_json()
        message = "The Email invalid@email.com does not belong to a valid viewer."
        self.assertEqual(message, json_data['message'])

    def test_url_without_match(self):
        """Ensure the URL has a recording associated"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        rv = self.has_access_recording(email, url, password)
        json_data = rv.get_json()
        message = "The URL " + url + " does not belong to a valid Recording."
        self.assertEqual(message, json_data['message'])

    def test_host_access_private_recording(self):
        """Ensure the host has access to the private recording of a meeting"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = True
        meeting_id = 1
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        rv = self.has_access_recording(email, url, password)
        json_data = rv.get_json()
        message = "SUCCESS: Viewer " + email + " has access to the Recording."
        self.assertEqual(message, json_data['message'])

    def test_viewer_access_private_recording(self):
        """Ensure the viewer does not have access to a private recording of a meeting"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = True
        meeting_id = 1
        email = "test@email.com"
        email_alt = "alternative@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_viewer(email_alt)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        rv = self.has_access_recording(email_alt, url, password)
        json_data = rv.get_json()
        message = "FAIL: Viewer " + email_alt + " does not have access to the Recording."
        self.assertEqual(message, json_data['message'])

    def test_viewer_access_public_recording(self):
        """Ensure the viewer knows the password and shares the public recording"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = False
        meeting_id = 1
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        self.share_recording(email, url)
        rv = self.has_access_recording(email, url, password)
        json_data = rv.get_json()
        message = "SUCCESS: Viewer " + email + " has access to the Recording."
        self.assertEqual(message, json_data['message'])

    def test_wrong_password_public_recording(self):
        """Ensure the password is correct for public recording"""
        url = "https://s3.amazonaws.com/meetings/recording1/"
        is_private = False
        meeting_id = 1
        email = "test@email.com"
        password = "pass"
        self.create_viewer(email)
        self.create_meeting(email, password)
        self.create_recording(url, is_private, meeting_id)
        self.share_recording(email, url)
        rv = self.has_access_recording(email, url, "wrongPass")
        json_data = rv.get_json()
        message = "FAIL: Viewer " + email + " does not have access to the Recording."
        self.assertEqual(message, json_data['message'])


if __name__ == '__main__':
    unittest.main()
