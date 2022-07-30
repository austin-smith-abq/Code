"""Data models."""
from . import db


class Location(db.Model):
    __tablename__ = 'location'
    location_guid = db.Column(
        db.Integer,
        primary_key=True
    )
    active = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )
    street_address = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    city = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    state = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    zip_code = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    latitude = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    longitude = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    
    
class Room(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'room'
    location_guid = db.Column(
        db.Integer, 
        db.ForeignKey('location.location_guid'),
        index=False,
        unique=False,
        nullable=True,
    )
    room_guid = db.Column(
        db.Integer,
        primary_key=True
    )
    floor = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    room_number = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    wasp_guid = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
