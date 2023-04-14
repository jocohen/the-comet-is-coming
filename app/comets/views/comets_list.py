import logging
from typing import Any, Dict

from comets.forms import SearchCometForm
from comets.nasa_service.NEOExplorer import NEOExplorer
from comets.nasa_service.schemas import NasaServiceError
from django.conf import settings
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class CometsListView(TemplateView):
    template_name = "comets/list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if (
            self.request.GET.get("from_date") is None
            and self.request.GET.get("to_date") is None
        ):
            # If coming without params do not show erros
            # @todo find better way to achieve this
            form = SearchCometForm()
        else:
            form = SearchCometForm(self.request.GET)

        comets = []
        if form.is_valid():
            from_date = form.cleaned_data.get("from_date")
            to_date = form.cleaned_data.get("to_date")
            context["from_date"] = from_date
            context["to_date"] = to_date

            service = NEOExplorer(settings.NASA_API_KEY)
            try:
                comets = service.get_neos_by_dates(from_date, to_date)
            except NasaServiceError as exc:
                logger.error(
                    "NasaServiceError when searching for comets                     "
                    f" in dates {from_date}/{to_date}.Exc message : {str(exc)}"
                )
                context.update(
                    {
                        "error_message": (
                            "Connection to the Nasa service encountered a problem."
                        )
                    }
                )

        context["search_form"] = form
        context["comets"] = comets
        return context
