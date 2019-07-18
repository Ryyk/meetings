

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


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
@app.route('/meeting', methods=['POST'])
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
@app.route('/meeting', methods=['GET'])
def get_meetings():
    all_meetings = models.Meeting.query.all()
    result = models.meetings_schema.dump(all_meetings)
    return jsonify(result.data)

# Get Single Meeting
@app.route('/meeting/<id>', methods=['GET'])
def get_meeting(id):
    meeting = models.Meeting.query.get(id)
    # Check if meeting exists
    if not meeting:
        return jsonify({"message": "Meeting with id " + id + " does not exist."})
    return models.meeting_schema.jsonify(meeting)


"""
This is the Recording API
"""

# Create a Recording
@app.route('/recording', methods=['POST'])
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
@app.route('/recording/delete/<path:url>', methods=['GET'])
def delete_recording(url):
    # Check if URL is valid 
    recording = db.session.query(models.Recording).get(url)
    if not recording:
        return jsonify({"message": "URL does not exist."})

    db.session.delete(recording)
    db.session.commit()
    return models.recording_schema.jsonify(recording)

# Share Recording
@app.route('/recording/share/<path:url>', methods=['PUT'])
def share_recording(url):
    return None

# Get All Recordings
@app.route('/recording', methods=['GET'])
def get_recordings():
    all_recordings = models.Recording.query.all()
    result = models.recordings_schema.dump(all_recordings)
    return jsonify(result.data)

# Get Single Recordings
@app.route('/recording/<path:url>', methods=['GET'])
def get_recording(url):
    recording = models.Recording.query.get(url)
    return models.recording_schema.jsonify(recording)


# Add Viewer to Recording
@app.route('/recording/add-viewer', methods=['POST'])
def add_viewer_to_recording():
    email = request.json['email']
    url = request.json['url']
    recording = db.session.query(models.Recording).get(url)
    viewer = db.session.query(models.Viewer).filter_by(email=email).first()

    if not recording or not viewer:
        return jsonify({"message": "Email or URL do not belong to a valid viewer or recording."})

    if recording.is_private:
        return jsonify({"message": "Cannot add a Viewer to a private Recording."})

    recording.viewers.append(viewer)
    db.session.add(recording)
    db.session.commit()

    result = models.viewers_schema.dump(recording.viewers)
    return jsonify(result.data)

# Get Viewers of a Recording
@app.route('/recording/get-viewers/<path:url>', methods=['GET'])
def get_viewers_recording(url):
    recording = models.Recording.query.get(url)

    # Recording not found
    if not recording:
        return jsonify({"message": "Recording not found."})

    result = models.viewers_schema.dump(recording.viewers)

    # Recording without Viewers
    if not result.data:
        return jsonify({"message": "No viewers associated with this recording."})

    return jsonify(result.data)

# Verify if a Viewer has access to a specific Recording
@app.route('/recording/has-access', methods=['GET'])
def verify_viewer_access():
    email = request.json['email']
    url = request.json['url']
    password = request.json['password']

    recording = db.session.query(models.Recording).get(url)
    viewer = db.session.query(models.Viewer).filter_by(email=email).first()

    return None


"""

This is the Viewers API

"""

# Create a Viewer
@app.route('/viewer', methods=['POST'])
def create_viewer():
    email = request.json['email']  # verify if it is a valid email @
    new_viewer = models.Viewer(email)

    db.session.add(new_viewer)
    db.session.commit()

    return models.viewer_schema.jsonify(new_viewer)

# Get All Viewers
@app.route('/viewer', methods=['GET'])
def get_viewers():
    all_viewers = models.Viewer.query.all()
    result = models.viewers_schema.dump(all_viewers)
    return jsonify(result.data)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
