from django import forms


class SearchCometForm(forms.Form):
    from_date = forms.DateField(label="From")
    to_date = forms.DateField(label="To")