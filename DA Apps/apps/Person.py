"""Data models."""
from . import db


class Person(db.Model):
    __tablename__ = 'person'
    person_guid = db.Column(
        db.Integer,
        primary_key=True
    )
    active = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )
    first_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    last_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    agency = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    primary_phone = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    cell_phone = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    personal_phone = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    primary_email = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    secondary_email = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    employee_id = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    bar_status = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=True
    )
    location_guid = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    cms_guid = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    evidence_guid = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    

    
class User(db.Model):
    """Data model for user accounts."""
    __tablename__ = 'user'
    person_guid = db.Column(
        db.Integer, 
        primary_key=True
    )
    user_guid = db.Column(
        db.Integer, 
        index=False,
        unique=False,
        nullable=True,
    )
    user_type = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    division = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    title = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    start_date = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    end_date = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    supervisor_guid = db.Column(
        db.Integer, 
        db.ForeignKey('person.person_guid'),
        index=False,
        unique=False,
        nullable=True,
    )
    rater_guid = db.Column(
        db.Integer, 
        db.ForeignKey('person.person_guid'),
        index=False,
        unique=False,
        nullable=True,
    )
    reviewer_guid = db.Column(
        db.Integer, 
        db.ForeignKey('person.person_guid'),
        index=False,
        unique=False,
        nullable=True,
    )
    room_guid = db.Column(
        db.Integer, 
        db.ForeignKey('room.room_guid'),
        index=False,
        unique=False,
        nullable=True,
    )
    wasp_guid = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )