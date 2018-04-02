import logging
import requests

from requests.exceptions import ReadTimeout, TooManyRedirects, ConnectionError
from app.constants import NETWORK_TIMEOUT

LOGGER = logging.getLogger(__name__)


def async_network_call(url):
    try:
        return requests.get(url, timeout=NETWORK_TIMEOUT)
    except ConnectionError:
        LOGGER.exception("Unable to connect to `{}`".format(url))
    except TooManyRedirects:
        LOGGER.exception("Too many redirects for `{}`".format(url))
    except ReadTimeout:
        LOGGER.exception("Connection timeout ({} s) exceeded for `{}`".format(NETWORK_TIMEOUT, url))
