"""Data models."""
from . import db
from .Database import *
from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    user_type: str
    user_id: str
    division: str
    title: str
    supervisor: bool
    database: str = "users"

    def __post_init__(self):
        self.email = (
            f"{self.first_name.lower()}.{self.last_name.lower()}@da2nd.state.nm.us"
        )

    def add(self):
        values = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_type": self.user_type,
            "user_id": self.user_id,
            "email": self.email,
            "division": self.division,
            "title": self.title,
            "supervisor": self.supervisor,
            "active": True,
        }
        Database.add(self.database, values)


@dataclass
class Contact:
    first_name: str
    last_name: str
    agency: str
    badge_id: str
    title: str
    primary_phone: str
    cell_phone: str
    email: str
    database: str = "contacts"

    def add(self):
        values = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "agency": self.agency,
            "badge_id": self.badge_id,
            "title": self.title,
            "primary_phone": self.primary_phone,
            "cell_phone": self.cell_phone,
            "email": self.email,
            "active": True,
        }
        Database.add(self.database, values)


class Person(db.Model):

    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=False, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    bio = db.Column(db.Text, index=False, unique=False, nullable=True)
    admin = db.Column(db.Boolean, index=False, unique=False, nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.username)
