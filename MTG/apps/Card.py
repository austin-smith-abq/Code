"""Data models."""
from . import db


class Card(db.Model):
    __tablename__ = 'magic_collection'
    card_id = db.Column(
        db.Integer,
        primary_key=True,
    )
    deck_id = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=True,
    )
    active = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )
    card_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
