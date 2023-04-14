from datetime import date

from comets.forms import SearchCometForm
from comets.views.comets_list import CometsListView
from django.shortcuts import resolve_url
from django.test import RequestFactory, TestCase


class CometsListViewTests(TestCase):
    url_list = resolve_url("comets:list")

    def test_list_view(self):
        date = "2020-01-01"
        response = self.client.get(self.url_list, {"from_date": date, "to_date": date})
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIn("comets", response.context)
        form = response.context.get("search_form")
        self.assertIs(type(form), SearchCometForm)
        self.assertEqual(form.is_bound, True)
        comets = response.context.get("comets")
        self.assertTrue(len(comets) > 0)

    def test_list_view_fail(self):
        with self.settings(NASA_API_KEY="failure"):
            date = "2020-01-01"
            response = self.client.get(
                self.url_list, {"from_date": date, "to_date": date}
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("search_form", response.context)
            self.assertIn("comets", response.context)
            self.assertIn("error_message", response.context)

    def test_search_form_in_context(self):
        date_input = "2020-01-01"
        request = RequestFactory().get(
            self.url_list, {"from_date": date_input, "to_date": date_input}
        )
        view = CometsListView()
        view.setup(request)
        context = view.get_context_data()
        self.assertIn("search_form", context)
        form: SearchCometForm = context.get("search_form")
        self.assertIs(type(form), SearchCometForm)
        self.assertEqual(form.is_bound, True)
        self.assertTrue(form.is_valid())
        from_date = form.cleaned_data.get("from_date")
        to_date = form.cleaned_data.get("to_date")
        date_obj = date.fromisoformat(date_input)
        self.assertEqual(from_date, date_obj)
        self.assertEqual(to_date, date_obj)
