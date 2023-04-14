import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List

from comets.nasa_service.NEOExplorer import NEOExplorer
from comets.nasa_service.schemas import NasaServiceError
from django.conf import settings
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class CometDetailView(TemplateView):
    template_name = "comets/detail.html"

    def get_context_data(
        self, id: int, date_ref: date = date.today(), n: int = 5, **kwargs: Any
    ) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        service = NEOExplorer(settings.NASA_API_KEY)
        try:
            comet = service.get_neo_by_id(id)
            last_approaches = self.get_last_n_approaches_by_date(
                comet.close_approaches, date_ref, n
            )
            context.update(
                {
                    "comet_loaded": comet.id,
                    "name": comet.name,
                    "diameter": comet.diameter_avg,
                    "is_hazardous": comet.is_hazardous,
                    "is_sentry": comet.is_sentry,
                    "last_approaches": last_approaches,
                    "date_ref": date_ref,
                }
            )
        except NasaServiceError as exc:
            logger.error(
                f"NasaServiceError getting detail of {id}. Exc message: {str(exc)}"
            )
            context.update(
                {
                    "error_message": (
                        "Connection to the Nasa service encountered a problem."
                    )
                }
            )

        return context

    def get_last_n_approaches_by_date(
        self,
        data: List,
        date_ref: date,
        n: int,
    ) -> List:
        """
        Get last n approach by a date reference\n
        This function search for the n approach encounters,
        for the n elem previous the date reference.\n

        Args:
            data (List): list of all the close approach of the comet
            date_ref (date): date reference to get the latest n approaches
            n (int): number of approaches to keep

        Returns:
            List: latest n approaches
        """
        # Midnight time for date reference
        datetime_ref = datetime.combine(date_ref, datetime.min.time(), None)
        zero_delta = timedelta()

        # We assume that the data inc is not sorted,
        # For time complexity, we dont sort the data list
        # Storing only the negative diff
        # between the close approach time and the date reference
        # negative diff -> previous date_ref / positive -> after
        diff_time = []
        for index, elem in enumerate(data):
            diff = elem.time - datetime_ref
            if diff < zero_delta:
                diff_time.append({"index_in_data": index, "diff": diff})

        # Sorting it based on the diff in descending order
        # The next n items in diff_time are our elems
        diff_time.sort(key=lambda elem: elem["diff"], reverse=True)

        last_approaches = []
        # In case there's less items at the end then n asked
        max_items = min(n, len(diff_time))
        for x in range(max_items):
            last_approaches.append(data[diff_time[x].get("index_in_data")])
        return last_approaches
