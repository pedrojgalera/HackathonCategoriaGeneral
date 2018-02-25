import json
import requests

API_KEY = '9d0abc285fae2073040f90645ac21c59'

class dummyAPI(object):
    BASE_URL = 'http://api.openweathermap.org/data/2.5/{api_name}?q={city}&APPID={api_key}&lang={lang}'

    def __init__(self, key=API_KEY):
        self.api_key = API_KEY

    def call_method(self, url_params):
        params = self.params_treatment(url_params)
        function = params.pop('function')
        return getattr(self, function)(params)

    def params_treatment(self, params):
        return {key: value[0] for key, value in params.items()}

    def popeye(self, url_params):
        api_name = 'weather'
        url = self.BASE_URL.format(api_key=self.api_key,
                                       api_name=api_name,
                                       **url_params)
        r = requests.get(url)
        """TRATAMIENTO DE JSON PARA LEKTA """
        r = json.loads(r.text)
        res = {
            'temp': r['main']['temp'],
            'humidity': r['main']['humidity'],
            'weather': r['weather'][0]['main']
        }
        return res

    def coords(self, url_params):
        api_name = 'weather'
        url = self.BASE_URL.format(api_key=self.api_key,
                                       api_name=api_name,
                                       **url_params)
        r = requests.get(url)
        r = json.loads(r.text)
        res = {
            'coord-lon': r['coord']['lon'],
            'coord-lat': r['coord']['lat'],
            'coord-country': r['sys']['country']
        }
        return res
