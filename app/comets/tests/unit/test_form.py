from comets.forms import SearchCometForm
from django.core.exceptions import NON_FIELD_ERRORS
from django.test import TestCase


class SearchCometFormTests(TestCase):
    def test_form_valid(self):
        data = {
            "from_date": "2020-01-01",
            "to_date": "2020-01-01",
        }
        form = SearchCometForm(data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_wrong_data(self):
        data = {
            "from_date": "ijoiwejr",
            "to_date": "iojewijfew",
        }
        form = SearchCometForm(data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_required(self):
        data_list = [{}, {"from_date": "2020-10-10"}, {"to_date": "2020-10-10"}]
        for data in data_list:
            form = SearchCometForm(data)
            self.assertFalse(form.is_valid())
            self.assertTrue(form.has_error(NON_FIELD_ERRORS, "dates_required"))

    def test_form_invalid_from_date_superior_to_to_date(self):
        data = {
            "from_date": "2020-01-05",
            "to_date": "2020-01-01",
        }
        form = SearchCometForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, "from_date_superior"))

    def test_form_invalid_date_diff_sup_7_days(self):
        data = {
            "from_date": "2020-01-01",
            "to_date": "2020-01-09",
        }
        form = SearchCometForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, "time_delta_max"))
