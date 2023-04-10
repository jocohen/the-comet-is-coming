from typing import Any, Dict

from django.views.generic import TemplateView

from ..forms import SearchCometForm


class CometComingView(TemplateView):
    """
    Parent class for home and lost views, use to populate
    context with value requested from NEOW Explorer to know
    if the comet is coming.
    """

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["the_end"] = False
        return context


class HomeView(CometComingView):
    template_name = "comets/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchCometForm()
        return context


class LostView(CometComingView):
    template_name = "comets/lost.html"
