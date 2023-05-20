from dataclasses import dataclass


@dataclass
class PointDTO:
    calories: float
    price: float
    color: str
    label: str