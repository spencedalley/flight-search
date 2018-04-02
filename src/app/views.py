import logging
from concurrent.futures import ThreadPoolExecutor, wait
from json import JSONDecodeError

from django.http import JsonResponse
from django.views import View

from app import worker
from app.constants import *

LOGGER = logging.getLogger(__name__)


class SearchFlights(View):

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=len(SEARCHRUNNER_SCRAPER_API_VALID_ARGS))

    def get(self, _):
        searchrunner_api_futures = []

        for url in SEARCHRUNNER_SCRAPER_API_ENDPOINTS:
            searchrunner_api_futures.append(self.executor.submit(worker.async_network_call, url))

        wait(searchrunner_api_futures, timeout=SEARCHRUNNER_WORKER_TIMEOUT)

        response_json_list = []

        for index, api_future in enumerate(searchrunner_api_futures):
            url = SEARCHRUNNER_SCRAPER_API_ENDPOINTS[index]

            if api_future.done() and api_future.result():
                try:
                    response_json = api_future.result().json()
                    if response_json.get("results") and type(response_json.get("results")) is list:
                        response_json_list.append(response_json.get("results"))
                    else:
                        LOGGER.warning("JSON response from endpoint `{}` has no `results` key or `results` value is not"
                                       " JSON array. Type at `results` key: `{}`"
                                       .format(url, response_json.get('results')))

                except JSONDecodeError:
                    result = api_future.result()
                    LOGGER.error("Invalid/No JSON received for endpoint `{}` with status code {}"
                                 .format(url, result.status_code), result.content)
                except AttributeError:
                    # should either get a None or requests.models.Response that has a valid .json() method
                    LOGGER.error("Invalid object received for endpoint `{}`".format(url), api_future.result())

        sorted_results = []
        intermediary_results = [l.pop(0) for l in response_json_list]

        while intermediary_results:
            index, element = min(enumerate(intermediary_results),
                                 key=lambda val: val[1].get("agony", float("infinity")))
            sorted_results.append(element)

            if not response_json_list[index]:
                # internal list is now empty, remove it from collection
                response_json_list.pop(index)
                intermediary_results.pop(index)
            else:
                intermediary_results[index] = response_json_list[index].pop(0)

        client_response_json = {
            "count": len(sorted_results),
            "results": sorted_results
        }

        try:
            return JsonResponse(client_response_json, status=200)
        except (JSONDecodeError, TypeError):
            LOGGER.error("Invalid JSON generated.", str(client_response_json))
            return JsonResponse({"error": "Error generating JSON"}, status=500)
