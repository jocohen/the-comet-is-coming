from typing import NamedTuple, List
from datetime import datetime


class CometCloseApproachData(NamedTuple):
    """When the comets is in close approach of the earth

    Attributes:
        time (datetime): when it happened
        velocity (str): in km/s
        distance (str): in km
        orbiting_body (str): which celestials it's in orbit
    """
    time: datetime
    velocity: float
    distance: float
    orbiting_body: str


class NEOCometDetail(NamedTuple):
    """Based on NEO service, data for the comet

    Attributes:
        id (int): NEO reference id
        name (str): name of comet
        diameter_avg (float): approx average diameter in meters
        is_hazardous (bool): if comet has hazardous materials
        is_sentry (bool): if it will hit earth
        close_approaches (List[CometCloseApproachData]): all the times the comet approached Earth
    """
    id: int
    name: str
    diameter_avg: int
    is_hazardous: bool
    is_sentry: bool
    close_approaches: List[CometCloseApproachData]
