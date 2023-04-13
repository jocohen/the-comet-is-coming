from typing import Dict, Any
from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class SearchCometForm(forms.Form):
    from_date = forms.DateField(
        label="From", required=False, widget=forms.DateInput(attrs={"type":"date", "required":""})
    )
    to_date = forms.DateField(
        label="To", required=False, widget=forms.DateInput(attrs={"type":"date", "required":""})
    )

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if from_date and to_date:
            delta = to_date - from_date
            if delta < timedelta():
                raise ValidationError(
                    _("From date cannot be superior to the To date"),
                    code="from_date_superior"
                )
            if delta > timedelta(days=7):
                raise ValidationError(
                    _("The time limit difference is of 7 days max"),
                    code="time_delta_max"
                )
        else:
            raise ValidationError(
                _("Both dates input are required"),
                code="date_require"
            )
