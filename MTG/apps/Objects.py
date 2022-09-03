"""Data models."""
from . import db
from sqlalchemy.orm import relationship


class Deck(db.Model):
    __tablename__ = 'decks'
    children = relationship("Card")
    id = db.Column(
        db.Integer,
        primary_key=True,
    )


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    deck_id = db.Column(
        db.Integer,
        db.ForeignKey('Deck.id')
    )
    tcg_player_id = db.Column(
        db.Integer,
        db.ForeignKey('TCG.card_id')
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


class TCG(db.Model):
    __tablename__ = 'tcg_cards'
    card_id = db.Column(
        db.Integer,
        primary_key=True,
    )
    categoryid = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=True,
    )
    groupid = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=True,
    )
    name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    cleanname = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    image_url = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    url = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    modifiedon = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
