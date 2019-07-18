from app import db, ma

# Meeting Class/Model
class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    recordings = db.relationship('Recording', backref='person', lazy=True)

    def __init__(self, password):
        self.password = password


# Recording Class/Model
class Recording(db.Model):
    url = db.Column(db.String(255), primary_key=True)
    is_private = db.Column(db.Boolean, nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'),
        nullable=False)

    def __init__(self, url, is_private, meeting_id):
        self.url = url
        self.is_private = is_private
        self.meeting_id = meeting_id


# Schemas
class MeetingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'password')

class RecordingSchema(ma.Schema):
    class Meta:
        fields = ('url', 'is_private', 'meeting_id')


# Init schema
meeting_schema = MeetingSchema(strict=True)
meetings_schema = MeetingSchema(many=True, strict=True)

recording_schema = RecordingSchema(strict=True)
recordings_schema = RecordingSchema(many=True, strict=True)
