from dataclasses import dataclass

@dataclass
class Info:
    id: str
    name: str
    country: str
    beer_type: str
    cost: float
    score: float
    strength: float
    conclusion: str
