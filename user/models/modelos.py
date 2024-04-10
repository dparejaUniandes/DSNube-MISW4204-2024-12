import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()

class TaskStatus(enum.Enum):
    UPLOADED = "uploaded"
    PROCESSED = "processed"

class User(db.Model):
    id = db.Column(db.Long, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Long, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum(TaskStatus))
    video_id = db.Column(db.Long, db.ForeignKey('video.id'), nullable=False)
    user_id = db.Column(db.Long, db.ForeignKey('user.id'), nullable=False)

class Video(db.Model):
    id = db.Column(db.Long, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    task = db.relationship('Task', uselist=False, backref='video', lazy=True)








