from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import re

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Configuration
DATABASE = "meetings.db"
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

import models

"""
This is the Meeting API
"""

# Create a Meeting
@app.route('/meeting/create', methods=['POST'])
def create_meeting():
    host_email = request.json['host_email']
    password = request.json['password']

    # Verify if the host email is from a valid host
    viewer = models.Viewer.query.filter_by(
        email=host_email).first()
    if not viewer:
        return jsonify({"message": "Invalid host email."})

    new_meeting = models.Meeting(host_email, password)
    db.session.add(new_meeting)
    db.session.commit()
    return models.meeting_schema.jsonify(new_meeting)

# Get All Meetings
@app.route('/meeting/get', methods=['GET'])
def get_meetings():
    all_meetings = models.Meeting.query.all()
    result = models.meetings_schema.dump(all_meetings)
    return jsonify(result.data)

# Get Single Meeting
@app.route('/meeting/get/<id>', methods=['GET'])
def get_meeting(id):
    meeting = models.Meeting.query.get(id)
    # Check if meeting exists
    if not meeting:
        return jsonify({"message": "Meeting with id " + id +
                        " does not exist."})
    return models.meeting_schema.jsonify(meeting)


"""
This is the Recording API
"""

# Create a Recording
@app.route('/recording/create', methods=['POST'])
def create_recording():
    url = request.json['url']
    is_private = request.json['is_private']
    meeting_id = request.json['meeting_id']

    # Check if URL already exists
    recording = models.Recording.query.filter_by(url=url).first()
    if recording:
        return jsonify({"message": "URL already exists."})

    # Check if meeting id is valid
    meeting = models.Meeting.query.filter_by(id=meeting_id).first()
    if not meeting:
        return jsonify({"message": "Invalid meeting id."})

    new_recording = models.Recording(url, is_private, meeting_id)
    db.session.add(new_recording)
    db.session.commit()
    return models.recording_schema.jsonify(new_recording)

# Delete Recording
@app.route('/recording/delete', methods=['DELETE'])
def delete_recording():
    url = request.json['url']
    # Check if URL is valid
    recording = db.session.query(models.Recording).get(url)
    if not recording:
        return jsonify({"message": "URL does not exist."})

    db.session.delete(recording)
    db.session.commit()
    return models.recording_schema.jsonify(recording)

# Share Recording
@app.route('/recording/share', methods=['POST'])
def share_recording():
    email = request.json['email']
    url = request.json['url']
    recording = db.session.query(models.Recording).get(url)
    viewer = db.session.query(models.Viewer).filter_by(email=email).first()

    # Invalid Email
    if not viewer:
        return jsonify({"message": "The Email " + email +
                        " does not belong to a valid viewer."})

    # Invalid URL
    if not recording:
        return jsonify({"message": "The URL " + url +
                        " does not belong to a valid Recording."})

    # Share meeting with same viewer twice
    if viewer in recording.viewers:
        return jsonify({"message": "Cannot share meeting:" + url +
                        " with the viewer " + email + " twice."})

    # Add viewer private recording
    if recording.is_private:
        return jsonify({"message": "Cannot add viewers to "
                        "a private Recording."})

    recording.viewers.append(viewer)
    db.session.add(recording)
    db.session.commit()

    return jsonify({"message": "Viewer " + email +
                    " added to recording " + url + "!"})

# Verify if a Viewer has access to a specific Recording
@app.route('/recording/has-access', methods=['GET'])
def check_access():
    email = request.json['email']
    url = request.json['url']
    recording = models.Recording.query.get(url)
    viewer = models.Viewer.query.filter_by(email=email).first()
    # If the recording is private the owner can access it without password
    try:
        password = request.json['password']
    except KeyError:
        if recording.is_private:
            pass

    # Invalid Email
    if not viewer:
        return jsonify({"message": "The Email " + email +
                        " does not belong to a valid viewer."})

    # Invalid URL
    if not recording:
        return jsonify({"message": "The URL " + url +
                        " does not belong to a valid Recording."})

    meeting = models.Meeting.query.get(recording.meeting_id)
    meeting_host_email = meeting.host_email
    meeting_password = meeting.password

    # Only the host can access a private recording
    if recording.is_private:
        if email == meeting_host_email:
            return jsonify({"message": "SUCCESS: Viewer " + email +
                            " has access to the Recording."})
        return jsonify({"message": "FAIL: Viewer " + email +
                        " does not have access to the Recording."})

    # The viewer needs to know the password to access a public recording
    # and needs to be in the list of viewers as well
    else:
        if password == meeting_password and viewer in recording.viewers:
            return jsonify({"message": "SUCCESS: Viewer " + email +
                            " has access to the Recording."})
        return jsonify({"message": "FAIL: Viewer " + email +
                        " does not have access to the Recording."})


# Get All Recordings
@app.route('/recording/get', methods=['GET'])
def get_recordings():
    all_recordings = models.Recording.query.all()
    result = models.recordings_schema.dump(all_recordings)
    return jsonify(result.data)

# Get Single Recordings
@app.route('/recording/get/<path:url>', methods=['GET'])
def get_recording(url):
    recording = models.Recording.query.get(url)
    return models.recording_schema.jsonify(recording)


"""
This is the Viewers API
"""

# Create a Viewer
@app.route('/viewer/create', methods=['POST'])
def create_viewer():
    EMAIL_REGEX = re.compile(
        r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
    email = request.json['email']

    # Invalid Email
    if not EMAIL_REGEX.match(email):
        return jsonify({"message": "Invalid email."})

    # Email exists
    email_exists = models.Viewer.query.filter_by(
        email=email).first()
    if email_exists:
        return jsonify({"message": "Email already in use."})

    new_viewer = models.Viewer(email)
    db.session.add(new_viewer)
    db.session.commit()

    return models.viewer_schema.jsonify(new_viewer)

# Get All Viewers
@app.route('/viewer/get', methods=['GET'])
def get_viewers():
    all_viewers = models.Viewer.query.all()
    result = models.viewers_schema.dump(all_viewers)
    return jsonify(result.data)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
