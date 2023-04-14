from comets.forms import SearchCometForm
from comets.nasa_service.service_errors import NasaServiceError
from comets.views.home import CometComingView, HomeView, LostView
from django.shortcuts import resolve_url
from django.test import RequestFactory, TestCase


class CometComingViewTests(TestCase):
    url_home = resolve_url("comets:home")

    def test_get_context_data(self):
        request = RequestFactory().get(self.url_home)
        view = CometComingView()
        view.setup(request)
        context = view.get_context_data()
        self.assertIn("the_end", context)

    def test_get_context_data_service_fail(self):
        request = RequestFactory().get(self.url_home)
        view = CometComingView()
        view.setup(request)
        with self.settings(NASA_API_KEY="failure"):
            context = view.get_context_data()
            self.assertIn("the_end", context)
            self.assertIn("error_message", context)
            self.assertIs(type(context.get("error_message")), str)

    def test_get_context_data_override_in_param(self):
        request = RequestFactory().get(self.url_home, {"override": True})
        view = CometComingView()
        view.setup(request)
        with self.settings(NASA_API_KEY="failure"):
            context = view.get_context_data()
            self.assertIn("the_end", context)
            self.assertEqual(context.get("the_end"), True)

    def test_is_the_comet_coming(self):
        view = CometComingView()
        try:
            result = view.is_the_comet_coming()
        except Exception:
            raise self.failureException
        self.assertIs(type(result), bool)

    def test_is_the_comet_coming_service_fails(self):
        view = CometComingView()
        with self.assertRaises(NasaServiceError):
            with self.settings(NASA_API_KEY="failure"):
                view.is_the_comet_coming()

    def test_is_the_comet_coming_override(self):
        view = CometComingView()
        try:
            with self.settings(NASA_API_KEY="failure"):
                view.is_the_comet_coming(True)
        except Exception:
            raise self.failureException


class HomeViewTests(TestCase):
    url_home = resolve_url("comets:home")

    def test_is_comet_coming_view_child(self):
        self.assertTrue(issubclass(HomeView, CometComingView))

    def test_view(self):
        response = self.client.get(self.url_home)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIn("the_end", response.context)

    def test_view_service_fail(self):
        with self.settings(NASA_API_KEY="failure"):
            response = self.client.get(self.url_home)
            self.assertEqual(response.status_code, 200)
            self.assertIn("search_form", response.context)
            self.assertIn("the_end", response.context)
            self.assertIn("error_message", response.context)

    def test_search_form_in_context(self):
        request = RequestFactory().get(self.url_home)
        view = HomeView()
        view.setup(request)
        context = view.get_context_data()
        self.assertIn("search_form", context)
        form: SearchCometForm = context.get("search_form")
        self.assertIs(type(form), SearchCometForm)
        self.assertEqual(form.is_bound, False)


class LostViewTests(TestCase):
    url_lost = resolve_url("comets:lost")

    def test_comet_coming_view_child(self):
        self.assertTrue(issubclass(LostView, CometComingView))

    def test_view(self):
        response = self.client.get(self.url_lost)
        self.assertEqual(response.status_code, 200)
        self.assertIn("the_end", response.context)

    def test_view_service_fail(self):
        with self.settings(NASA_API_KEY="failure"):
            response = self.client.get(self.url_lost)
            self.assertEqual(response.status_code, 200)
            self.assertIn("the_end", response.context)
            self.assertIn("error_message", response.context)
