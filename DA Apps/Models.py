import database
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
        database.add(self.database, values)

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
        database.add(self.database, values)
