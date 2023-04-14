import datetime

from comets.nasa_service.abstract_explorer import AbstractExplorer
from comets.nasa_service.nasa_api_access import NasaAPIAccess
from comets.nasa_service.neo_explorer import NEOExplorer
from comets.nasa_service.schemas import NEOCometDetail
from comets.nasa_service.service_errors import NasaServiceError
from django.conf import settings
from django.test import TestCase


class NasaAPITestCase(TestCase):
    def get_nasa_api_key(self, success: bool = True) -> str:
        return settings.NASA_API_KEY if success else "weoifjfew"

    def get_nasa_service_api(self, success: bool = True) -> str:
        explorer = self.get_neo_explorer()
        return explorer.get_service_endpoint() if success else "/feoijfe/ewiojr"

    def get_nasa_api_access_object(self, success: bool = True) -> NasaAPIAccess:
        return NasaAPIAccess(
            self.get_nasa_api_key(success), self.get_nasa_service_api(success)
        )

    def get_neo_explorer(self, success: bool = True) -> NEOExplorer:
        return NEOExplorer(self.get_nasa_api_key(success))


class NasaAPIAccessTests(NasaAPITestCase):
    def test_init(self):
        data_access = self.get_nasa_api_access_object()
        self.assertEqual(data_access.api_key, self.get_nasa_api_key())
        self.assertEqual(data_access.service, self.get_nasa_service_api())
        self.assertIs(type(data_access.NASA_BASE_URL), str)

    def test_forge_url(self):
        data_access = self.get_nasa_api_access_object()
        endpoint = "/ko"
        expected = data_access.NASA_BASE_URL + self.get_nasa_service_api() + endpoint
        self.assertEqual(data_access.forge_url(endpoint), expected)

    def test_get_successful(self):
        dynamic = "/feed"
        data_access = self.get_nasa_api_access_object()
        try:
            data = data_access.get(dynamic)
        except Exception:
            raise self.failureException
        self.assertTrue(data)

    def test_get_fails_with_wrong_key(self):
        dynamic = "/feed"
        data_access = self.get_nasa_api_access_object(False)
        with self.assertRaises(NasaServiceError):
            data_access.get(dynamic)


class ExplorerTest(AbstractExplorer):
    def get_service_endpoint(self) -> str:
        return "/popopo"


class AbstractExplorerTests(TestCase):
    def test_init(self):
        api_key = "koko"
        explorer = ExplorerTest(api_key)
        self.assertIs(type(explorer.data_access), NasaAPIAccess)
        self.assertIs(explorer.data_access.api_key, api_key)
        self.assertIs(explorer.data_access.service, explorer.get_service_endpoint())

    def test_get_service_endpoint(self):
        explorer = ExplorerTest("koko")
        self.assertIs(explorer.get_service_endpoint(), "/popopo")


class NEOExplorerTests(NasaAPITestCase):
    def test_get_neo_by_dates_success(self):
        explorer = self.get_neo_explorer()
        past_date = datetime.date.fromisoformat("2020-10-10")
        try:
            data = explorer.get_neos_by_dates(past_date, past_date)
        except Exception:
            raise self.failureException

        self.assertIs(type(data), list)
        self.assertTrue(len(data) > 0)
        for elem in data:
            self.assertIs(type(elem), NEOCometDetail)

    def test_get_neo_by_dates_success_empty(self):
        explorer = self.get_neo_explorer()
        past_date = datetime.date.fromisoformat("1800-10-10")
        try:
            data = explorer.get_neos_by_dates(past_date, past_date)
        except Exception:
            raise self.failureException

        self.assertIs(type(data), list)
        self.assertTrue(len(data) == 0)

    def test_get_neo_by_dates_fail(self):
        explorer = self.get_neo_explorer(False)
        past_date = datetime.date.fromisoformat("2020-10-10")
        with self.assertRaises(NasaServiceError):
            explorer.get_neos_by_dates(past_date, past_date)

    def test_get_neo_by_dates_fail_date_diff_supp_7_dats(self):
        explorer = self.get_neo_explorer()
        start_date = datetime.date.fromisoformat("2020-10-10")
        end_date = datetime.date.fromisoformat("2020-10-20")
        with self.assertRaises(NasaServiceError):
            explorer.get_neos_by_dates(start_date, end_date)

    def test_get_neo_by_id_success(self):
        explorer = self.get_neo_explorer()
        comet_id_success = 2085770
        try:
            data = explorer.get_neo_by_id(comet_id_success)
        except Exception:
            raise self.failureException
        self.assertIs(type(data), NEOCometDetail)
        self.assertEqual(data.id, comet_id_success)

    def test_get_neo_by_id_fail(self):
        explorer = self.get_neo_explorer()
        comet_id_fail = 123987182937982
        with self.assertRaises(NasaServiceError):
            explorer.get_neo_by_id(comet_id_fail)

    def test_map_data_to_comet_detail_success(self):
        # @todo implement json fake data
        pass

    def test_map_data_to_comet_detail_fail(self):
        # @todo implement json fake data
        pass

    def test_map_data_to_close_approach_succes(self):
        # @todo implement json fake data
        pass

    def test_map_data_to_close_approach_fail(self):
        # @todo implement json fake data
        pass

    def test_convert_epoch_to_datetime(self):
        explorer = self.get_neo_explorer()
        epoch = 1602301980000
        result = datetime.datetime.fromtimestamp(1602301980)
        self.assertEqual(explorer.convert_epoch_to_datetime(epoch), result)

    def test_calculate_diameter_average(self):
        explorer = self.get_neo_explorer()
        min = 2.5
        max = 47.223
        result = round((min + max) / 2)
        self.assertEqual(explorer.calculate_diameter_average(min, max), result)
