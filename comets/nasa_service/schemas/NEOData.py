from typing import NamedTuple, List
from datetime import datetime


class CometCloseApproachData(NamedTuple):
    datetime: datetime
    velocity: str
    distance: str
    orbiting_body: str


class NEOCometDetail(NamedTuple):
    id: str
    name: str
    diameter_min: float
    diameter_max: float
    is_hazardous: bool
    is_sentry: bool
    close_approachs: List[CometCloseApproachData]
