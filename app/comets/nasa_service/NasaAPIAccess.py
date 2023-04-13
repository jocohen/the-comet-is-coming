from typing import Dict, Any

import requests

from comets.nasa_service.schemas import NasaServiceError


class NasaAPIAccess:
    """
    Class used to access Nasa api with general use case.\n
    In the future we can add an DataAccess abstract to implement
    multiple data sources (other framework to access an API)
    """
    NASA_BASE_URL = "https://api.nasa.gov"


    def __init__(self, api_key: str, api_service: str) -> None:
        """
        Init the class with the api_key and the service endpoint

        Args:
            api_key (str): nasa api_key
            api_service (str): nasa service endpoint
        """
        super().__init__()
        self.api_key = api_key
        self.service = api_service


    def get(self, endpoint: str, payload: Dict = {}) -> Any:
        """
        Get the nasa api on the final endpoint specified with the according
        payload

        Args:
            endpoint (str): dynamic endpoint
            payload (Dict): dict of all the parameters sent with the request
        
        Raises:
            NasaServiceError: when http error occured or json is invalid

        Returns:
            Any: response content loaded with json encoder
        """
        payload["api_key"] = self.api_key
        response = requests.get(self.forge_url(endpoint), params=payload)
        try:
            response.raise_for_status()
            data = response.json()
        except requests.HTTPError as exc:
            code = response.status_code
            raise NasaServiceError(f"HTTP Code : {code}, Exception message {str(exc)}")
        except requests.JSONDecodeError:
            raise NasaServiceError("Invalid json received")
        return data


    def forge_url(self, endpoint: str) -> str:
        return self.NASA_BASE_URL + self.service + endpoint
