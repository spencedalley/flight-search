from json import JSONDecodeError

from requests.exceptions import ReadTimeout, TooManyRedirects, ConnectionError


def timeout_effect(url, timeout):
    raise ReadTimeout


def too_many_redirects_effect(url, timeout):
    raise TooManyRedirects


def connection_error_effect(url, timeout):
    raise ConnectionError


class MockValidData:

    def __init__(self):
        pass

    def json(self):
        return {"results": [
            {
                "agony": 1,
                "price": 1999,
                "provider": "Expedia",
                "arrive_time": "2018-04-02T04:39:00",
                "flight_num": "UA1001",
                "depart_time": "2018-04-02T03:39:00"
            },
            {
                "agony": 2,
                "price": 1999,
                "provider": "Orbitz",
                "arrive_time": "2018-04-02T04:39:00",
                "flight_num": "UA1001",
                "depart_time": "2018-04-02T03:39:00"
            },
            {
                "agony": 3,
                "price": 1999,
                "provider": "Priceline",
                "arrive_time": "2018-04-02T04:39:00",
                "flight_num": "UA1001",
                "depart_time": "2018-04-02T03:39:00"
            }
        ]}


class MockEmptyData:

    def __init__(self):
        pass

    def json(self):
        return {"results": []}


class MockJsonDecodeError:

    def __init__(self):
        pass

    def json(self):
        raise JSONDecodeError(None, None, None)


class MockNoJsonMethodError:

    def __init__(self):
        pass

    def json(self):
        raise AttributeError(None, None, None)


