from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from typing import Any

import enum

db = SQLAlchemy()

class TaskStatus(enum.Enum):
    UPLOADED = "uploaded"
    PROCESSED = "processed"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.UPLOADED)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class EnumADiccionario(fields.Field):
    def _serialize(self, value: Any, attr: str | None, obj: Any, **kwargs):
        if value is None:
            return None
        return value.value

class TaskSchema(SQLAlchemyAutoSchema):
    status = EnumADiccionario(attribute=('status'))
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
