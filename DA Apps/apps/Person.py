"""Data models."""
from . import db


class Person(db.Model):
    __abstract__ = True
    id = db.Column(
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
    #primary_phone = db.Column(
    #    db.String(64),
    #    index=False,
    #    unique=False,
    #    nullable=True
    #)
    #cell_phone = db.Column(
    #    db.String(64),
    #    index=False,
    #    unique=False,
    #    nullable=True
    #)
    email = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    
class User(Person):
    """Data model for user accounts."""

    __tablename__ = 'users'
    user_type = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    user_id = db.Column(
        db.String(64),
        index=False,
        unique=True,
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
    supervisor = db.Column(
        db.Boolean,
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

class Contact(Person):
    """Data model for office contacts."""

    __tablename__ = 'contacts'
    agency = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    badge_id = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )