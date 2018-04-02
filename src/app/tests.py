import json
from unittest.mock import patch

from django.test import RequestFactory, TestCase

from app.constants import SEARCHRUNNER_SCRAPER_API_ENDPOINTS
from app.side_effects import *
from app.views import SearchFlights


class SearchFlightsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch("app.worker.LOGGER")
    @patch("requests.get", side_effect=connection_error_effect)
    def test_connection_error(self, mock_logger, _):
        request = self.factory.get('/flights/search')
        response = SearchFlights().get(request)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'count': 0, 'results': []})

    @patch("app.worker.LOGGER")
    @patch("requests.get", side_effect=timeout_effect)
    def test_timeout_error(self, mock_logger, _):
        request = self.factory.get('/flights/search')
        response = SearchFlights().get(request)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'count': 0, 'results': []})

    @patch("app.worker.LOGGER")
    @patch("requests.get", side_effect=too_many_redirects_effect)
    def test_too_many_redirects_error(self, mock_logger, _):
        request = self.factory.get('/flights/search')
        response = SearchFlights().get(request)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'count': 0, 'results': []})

    @patch("requests.get")
    def test_valid_data_returned(self, external_api_mock):
        external_api_mock.return_value = MockValidData()
        request = self.factory.get('/flights/search')
        response = SearchFlights().get(request)
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response.get("count"),
                         len(SEARCHRUNNER_SCRAPER_API_ENDPOINTS) * len(MockValidData().json().get("results")))

        items = json_response.get("results")
        previous_agony = None

        for item in items:
            current_agony = item.get("agony")
            if previous_agony:
                self.assertLessEqual(previous_agony, current_agony)
            previous_agony = current_agony

    @patch("app.views.LOGGER")
    @patch("requests.get")
    def test_empty_data_returned(self, mock_logger, external_api_mock):
        external_api_mock.return_value = MockEmptyData()
        request = self.factory.get('/flights/search')
        response = SearchFlights().get(request)
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response.get("count"), 0)
        self.assertEqual(json_response.get("results"), [])

    @patch("app.views.LOGGER")
    @patch("requests.get")
    def test_unexpected_data_type_returned(self, mock_logger, external_api_mock):
        external_api_mock.return_value = MockJsonDecodeError()
        request = self.factory.get('/flights/search')
        response = SearchFlights().get(request)
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response.get("count"), 0)
        self.assertEqual(json_response.get("results"), [])

    @patch("app.views.LOGGER")
    @patch("requests.get")
    def test_no_json_method(self, mock_logger, external_api_mock):
        external_api_mock.return_value = MockNoJsonMethodError()
        request = self.factory.get('/flights/search')
        response = SearchFlights().get(request)
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response.get("count"), 0)
        self.assertEqual(json_response.get("results"), [])




