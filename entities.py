from dataclasses import dataclass
from datetime import datetime, date
from typing import List


@dataclass
class Flight:
    position: int
    country: str
    player: str
    time: float
    green_delta: float
    delta: float
    drone: str
    date: datetime
    updates: int


@dataclass
class Leaderboard:
    season: int
    date: date
    map: str
    track: str
    flights: List[Flight] = None