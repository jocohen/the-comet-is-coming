import logging
from datetime import date
from typing import Any, Dict

from comets.forms import SearchCometForm
from comets.nasa_service.NEOExplorer import NEOExplorer
from comets.nasa_service.schemas import NasaServiceError
from django.conf import settings
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class CometComingView(TemplateView):
    """
    Parent class for home and lost views, use to populate
    context with data requested from NEO Explorer about today's comets
    to know if the comet is coming.
    """

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        the_end = False
        try:
            the_end = self.is_the_comet_coming(
                self.request.GET.get("override", False) is not False
            )
        except NasaServiceError as exc:
            logger.critical(str(exc))
            context.update(
                {
                    "error_message": (
                        "Connection to the Nasa service encountered a problem."
                    )
                }
            )

        context["the_end"] = the_end
        return context

    def is_the_comet_coming(self, override: bool = False) -> bool:
        if override:
            return True

        service = NEOExplorer(settings.NASA_API_KEY)
        today = date.today()
        data = service.get_neos_by_dates(today, today)

        is_it_coming = False
        for comet in data:
            if comet.is_hazardous and comet.is_sentry:
                is_it_coming = True
        return is_it_coming


class HomeView(CometComingView):
    template_name = "comets/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchCometForm()
        return context


class LostView(CometComingView):
    template_name = "comets/lost.html"
