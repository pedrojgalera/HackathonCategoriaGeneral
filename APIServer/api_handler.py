import json
import requests


CREDENTIALS_PATH = 'credentials.json'


class APIHandler(object):

    def __init__(self, api_name, credentials=CREDENTIALS_PATH):
        with open(credentials) as cred:
            api_cred = json.load(cred)[api_name]

        self.api_key = api_cred.get("API_KEY", None)
        self.key_coor = api_cred.get("KEY_COORDINATES", None)
        self.key_dist = api_cred.get("KEY_DISTANCES", None)
        self.url = api_cred.get("URL", None)
        self.client_id = api_cred.get("CLIENT_ID", None)
        self.client_secret = api_cred.get("CLIENT_SECRET", None)
        self.version = api_cred.get("VERSION", None)
        self.geo = api_cred.get("GEO", None)

    def __call_method__(self, url_params):
        params = self.__params_treatment__(url_params)
        function = params['function']
        return getattr(self, function)(params)


    def __params_treatment__(self, params):
        return {key: value[0] for key, value in params.items()}

    def __api_get__(self, url, params=None):
        r = requests.get(url, params)
        res = json.loads(r.text)
        return res

    def __get_functions_map__(self):
        return {method: self.__class__ for method in filter(lambda x: x[0] != '_' and x not in self.__dict__, self.__dir__())}
