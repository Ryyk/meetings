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
    host_email = request.json['host_email'] #verify if the host email is a valid "host" if not exception
    password = request.json['password']
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
    return models.meeting_schema.jsonify(meeting)

"""

This is the Recording API

"""

# Create a Recording
@app.route('/recording', methods=['POST'])
def create_recording():
    url = request.json['url']
    is_private = request.json['is_private']
    meeting_id = request.json['meeting_id'] #validate meeting id (real meeting?)
    new_recording = models.Recording(url, is_private, meeting_id)

    db.session.add(new_recording)
    db.session.commit()

    return models.recording_schema.jsonify(new_recording)

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

# Delete Recording
@app.route('/recording/<path:url>', methods=['DELETE'])
def delete_recording(url):
  recording = db.session.query(models.Recording).get(url)
  db.session.delete(recording)
  db.session.commit()

  return models.recording_schema.jsonify(recording)

"""

This is the Viewers API

"""

# Create a Viewer
@app.route('/viewer', methods=['POST'])
def create_viewer():
    email = request.json['email'] #verify if it is a valid email @
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
