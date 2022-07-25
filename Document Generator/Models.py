import database
from dataclasses import dataclass

@dataclass
class Employee:
    first_name: str
    last_name: str
    employee_id: str
    division: str
    title: str
    database: str = 'employees'

    def __post_init__(self):
        self.email = f'{self.first_name.lower()}.{self.last_name.lower()}@da2nd.state.nm.us'

    def add(self):
        values = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'employee_id': self.employee_id,
            'email': self.email,
            'division': self.division,
            'title': self.title,
            'active': True,
        }
        database.add(self.database, values)
