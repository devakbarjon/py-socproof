from dataclasses import dataclass


@dataclass
class Service:
    service: int
    name: str
    type: str
    rate: float
    min: int
    max: int
    refill: bool
    cancel: bool
    category: str = ""
    description: str = ""  # ru
    time: str = ""


@dataclass
class OrderStatus:
    order_id: str
    charge: float
    status: str
    remains: int
