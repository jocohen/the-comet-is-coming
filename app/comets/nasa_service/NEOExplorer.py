import datetime
import json
from typing import Any, List

from comets.nasa_service.AbstractExplorer import AbstractExplorer
from comets.nasa_service.schemas import (
    CometCloseApproachData,
    NasaServiceError,
    NEOCometDetail,
)


class NEOExplorer(AbstractExplorer):
    """Service to access Nasa Near Eath Object API

    Constructors:
    __new__()

    Methods:
    get_neos_by_dates()
    get_neo_by_id()

    """

    LIST_ENDPOINT = "/feed"
    LOOKUP_ENDPOINT = "/neo"

    def get_service_endpoint(self) -> str:
        return "/neo/rest/v1"

    def get_neos_by_dates(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> List[NEOCometDetail]:
        """Get NEOs by a start_date and an end_date

        Args:
            start_date (datetime.date)
            end_date (datetime.date)

        Raises:
            NasaServiceError: when the sourcing of the data had
            a problem (info in the exc)

        Returns:
            List[NEOCometDetail]: list of neos
        """
        data = self.data_access.get(
            self.LIST_ENDPOINT,
            {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
        )

        data = data.get("near_earth_objects", {}).values()

        comet_list = []
        for comets in data:
            for comet in comets:
                comet_list.append(self.map_data_to_comet_detail(comet))
        return comet_list

    def get_neo_by_id(self, comet_id: str) -> NEOCometDetail:
        """Get more info on one NEO by id

        Args:
            comet_id (int)

        Raises:
            NasaServiceError: when the sourcing of the data had
            a problem (info in the exc)


        Returns:
            NEOCometDetail
        """
        data = self.data_access.get(self.LOOKUP_ENDPOINT + "/" + str(comet_id))

        return self.map_data_to_comet_detail(data)

    def map_data_to_comet_detail(self, raw: dict) -> NEOCometDetail:
        """
        Map raw data of a NEO to DAO format.

        Args:
            raw (dict)

        Raises:
            NasaServiceError: when the data is invalid

        Returns:
            NEOCometDetail
        """
        try:
            comet = NEOCometDetail(
                id=int(get(raw, str, "neo_reference_id")),
                name=get(raw, str, "name"),
                diameter_avg=self.calculate_diameter_average(
                    min=get(
                        raw,
                        float,
                        "estimated_diameter",
                        "meters",
                        "estimated_diameter_min",
                    ),
                    max=get(
                        raw,
                        float,
                        "estimated_diameter",
                        "meters",
                        "estimated_diameter_max",
                    ),
                ),
                is_hazardous=get(raw, bool, "is_potentially_hazardous_asteroid"),
                is_sentry=get(raw, bool, "is_sentry_object"),
                close_approaches=self.map_data_to_close_approach(
                    get(raw, list, "close_approach_data")
                ),
            )

            return comet

        except (ValueError, TypeError):
            raise NasaServiceError(f"Invalid data:{json.dumps(raw)}")

    def map_data_to_close_approach(
        self, data: List[dict]
    ) -> List[CometCloseApproachData]:
        """Map raw data of all close approaches to DAO format

        Args:
            data (List[dict])

        Returns:
            List[CometCloseApproachData]
        """
        mapped_data = []
        for raw in data:
            mapped_data.append(
                CometCloseApproachData(
                    time=self.convert_epoch_to_datetime(
                        get(raw, int, "epoch_date_close_approach")
                    ),
                    velocity=float(
                        get(raw, str, "relative_velocity", "kilometers_per_second")
                    ),
                    distance=float(get(raw, str, "miss_distance", "kilometers")),
                    orbiting_body=get(raw, str, "orbiting_body"),
                )
            )
        return mapped_data

    def convert_epoch_to_datetime(self, epoch: int) -> datetime.datetime:
        """
        Convert epoch in millisec to datetime in sec

        Args:
            epoch (int): timestamp to convert

        Returns:
            datetime.datetime
        """
        return datetime.datetime.fromtimestamp(epoch / 1000)

    def calculate_diameter_average(self, min: float, max: float) -> int:
        return round((min + max) / 2)


def get(data: Any, data_type: type, *keys: str) -> Any:
    """
    Basic geter of values in dicts
    It works with nested values
    It also checks for the type of the value getted

    Args:
        data (Any): dict
        data_type (type): the type to check for the data getted
        *keys (str): all the keys to get to the wanted data

    Raises:
        ValueError: when the key in the dict doesn't exist
        TypeError: when the data getted isn't of the type to check

    Returns:
        Any: data getted
    """
    if isinstance(data, dict) is False:
        raise TypeError
    for key in keys:
        if key in data:
            data = data[key]
        else:
            raise ValueError
    if isinstance(data, data_type) is False:
        raise TypeError
    return data
