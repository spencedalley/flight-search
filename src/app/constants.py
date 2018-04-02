# searchrunner site details
SEARCHRUNNER_DOMAIN = "http://localhost:9000"
SEARCHRUNNER_SCRAPER_API = "{}/scrapers".format(SEARCHRUNNER_DOMAIN)
SEARCHRUNNER_SCRAPER_API_VALID_ARGS = ("expedia", "orbitz", "priceline", "travelocity", "united")
SEARCHRUNNER_SCRAPER_API_ENDPOINTS = tuple(("{}/{}".format(SEARCHRUNNER_SCRAPER_API, arg)
                                            for arg in SEARCHRUNNER_SCRAPER_API_VALID_ARGS))

# timeouts in seconds
NETWORK_TIMEOUT = 10
SEARCHRUNNER_WORKER_TIMEOUT = 20






