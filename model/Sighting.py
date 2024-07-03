from dataclasses import dataclass
import datetime


@dataclass
class Sighting:
    id: int
    datetime: datetime
    city: str
    state: str
    country: str
    shape: str
    duration: int
    duration_hm: str
    comments: str
    date_posted: datetime
    latitude: float
    longitude: float

    def __str__(self):
        return f"id: {self.id}, datetime: {self}"

    def __hash__(self):
        return hash(self.id)
