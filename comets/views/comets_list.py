import logging
from typing import Any, Dict

from django import http
from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import TemplateView

from comets.forms import SearchCometForm

from comets.nasa_service.NEOExplorer import NEOExplorer
from comets.nasa_service.schemas import NasaServiceError


logger = logging.getLogger(__name__)


class CometsListView(TemplateView):
    template_name = "comets/list.html"


    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        # Check for validity of form and redirect if it's not valid
        self.form = SearchCometForm(request.GET)
        if not self.form.is_valid():
            return redirect("comets:home")

        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        from_date = self.form.cleaned_data.get("from_date")
        to_date = self.form.cleaned_data.get("to_date")

        service = NEOExplorer(settings.NASA_API_KEY)
        try:
            comets = service.get_neos_by_dates(from_date, to_date)
        except NasaServiceError as exc:
            logger.error(
                f"NasaServiceError when searching for comets in dates {from_date}/{to_date}.Exc message : {str(exc)}"
            )
            # @todo handle error
            comets = []

        context["comets"] = comets
        context["max_date"] = to_date
        return context
