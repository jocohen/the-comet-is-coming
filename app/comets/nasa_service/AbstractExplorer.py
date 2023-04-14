from abc import ABC, abstractmethod

from comets.nasa_service.NasaAPIAccess import NasaAPIAccess


class AbstractExplorer(ABC):
    """Abstract class to have multiple explorers.\n
    An explorer class is a service that has a NasaAPIAccess object in his properties,
    initialized based on the get_service_endpoint
    method that has to be implemented by child.\n

    This is designed to have an implementation of multiple Nasa APIs
    with a correct level of abstraction and\n
    also that the explorer has no idea of what is the type of data_access he has.
    """

    def __init__(self, api_key: str) -> None:
        super().__init__()
        self.data_access = NasaAPIAccess(
            api_key=api_key, api_service=self.get_service_endpoint()
        )

    @abstractmethod
    def get_service_endpoint(self) -> str:
        pass
