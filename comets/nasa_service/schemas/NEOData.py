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
    velocity: str
    distance: str
    orbiting_body: str


class NEOCometDetail(NamedTuple):
    """Based on NEO service, data for the comet

    Attributes:
        id (str): NEO reference id
        name (str): name of comet
        diameter_min (float): approx min diameter in meters
        diameter_max (float): approx max diameter in meters
        is_hazardous (bool): if comet has hazardous materials
        is_sentry (bool): if it will hit earth
        close_approachs (List[CometCloseApproachData]): all the times the comet approached Earth
    """
    id: str
    name: str
    diameter_min: float
    diameter_max: float
    is_hazardous: bool
    is_sentry: bool
    close_approachs: List[CometCloseApproachData]
