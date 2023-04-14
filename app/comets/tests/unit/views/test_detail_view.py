from datetime import date

from django.shortcuts import resolve_url
from django.test import TestCase


class CometDetailViewTest(TestCase):
    detail_view_path = "comets:detail"
    comet_id_success = 2085770

    def test_full_detail_view(self):
        date_input = date.fromisoformat("2020-02-02")
        n_input = 15
        response = self.client.get(
            resolve_url(
                to=self.detail_view_path,
                id=self.comet_id_success,
                date_ref=date_input,
                n=n_input,
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("comet_loaded", response.context)
        self.assertIn("name", response.context)
        self.assertIn("diameter", response.context)
        self.assertIn("is_hazardous", response.context)
        self.assertIn("is_sentry", response.context)
        self.assertIn("last_approaches", response.context)
        self.assertIn("date_ref", response.context)
        comet_loaded = response.context.get("comet_loaded")
        date_ref = response.context.get("date_ref")
        approaches = response.context.get("last_approaches")
        self.assertIs(type(approaches), list)
        self.assertEqual(comet_loaded, self.comet_id_success)
        self.assertEqual(date_ref, date_input)
        self.assertEqual(n_input, len(approaches))

    def test_detail_view_fail(self):
        with self.settings(NASA_API_KEY="failure"):
            date_input = date.fromisoformat("2020-02-02")
            n_input = 15
            response = self.client.get(
                resolve_url(
                    to=self.detail_view_path,
                    id=self.comet_id_success,
                    date_ref=date_input,
                    n=n_input,
                )
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("error_message", response.context)

    def test_detail_view_param_default(self):
        response = self.client.get(
            resolve_url(to=self.detail_view_path, id=self.comet_id_success)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("comet_loaded", response.context)
        self.assertIn("last_approaches", response.context)
        self.assertIn("date_ref", response.context)
        comet_loaded = response.context.get("comet_loaded")
        date_ref = response.context.get("date_ref")
        approaches = response.context.get("last_approaches")
        self.assertIs(type(approaches), list)
        self.assertEqual(comet_loaded, self.comet_id_success)
        self.assertEqual(date_ref, date.today())
        self.assertTrue(len(approaches) <= 5)
