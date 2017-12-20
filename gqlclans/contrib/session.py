from collections import defaultdict

import requests


class PapiRequestSession:
    session = None
    adapters = {}
    store = defaultdict(list)

    def __init__(self):
        self.session = requests.Session()
        for url, adapter in PapiRequestSession.adapters.items():
            self.session.mount(url, adapter)
