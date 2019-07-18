from app import db, ma

# Meeting Class/Model
class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    recordings = db.relationship('Recording', backref='meeting', lazy=True, uselist=False)

    def __init__(self, host_email, password):
        self.host_email = host_email
        self.password = password


# Recording Class/Model
class Recording(db.Model):
    url = db.Column(db.String(255), primary_key=True)
    is_private = db.Column(db.Boolean, nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'),
        nullable=False)

    viewers = db.relationship('Viewer', secondary="viewers", lazy='subquery',
        backref=db.backref('recordings', lazy=True))

    def __init__(self, url, is_private, meeting_id):
        self.url = url
        self.is_private = is_private
        self.meeting_id = meeting_id

# Viewer Class/Model
class Viewer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, email):
        self.email = email


# Helper table
viewers = db.Table('viewers',
    db.Column('recording_url', db.String(255), db.ForeignKey('recording.url'), primary_key=True),
    db.Column('viewer_email', db.String(100), db.ForeignKey('viewer.email'), primary_key=True)
)

# Schemas
class MeetingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'host_email', 'password')

class RecordingSchema(ma.Schema):
    class Meta:
        fields = ('url', 'is_private', 'meeting_id', 'viewers')

class ViewerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email')


# Init schema
meeting_schema = MeetingSchema(strict=True)
meetings_schema = MeetingSchema(many=True, strict=True)

recording_schema = RecordingSchema(strict=True)
recordings_schema = RecordingSchema(many=True, strict=True)

viewer_schema = ViewerSchema(strict=True)
viewers_schema = ViewerSchema(many=True, strict=True)
