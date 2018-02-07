from weather.forecast_helper import ForecastHelper
from api_handler import APIHandler


class WeatherAPI(APIHandler):

    def __init__(self):
        super().__init__(self.__class__.__name__)


    def __kelvin_to_celsius__(self, kelvin):
        return kelvin - 273.15


    def __url_builder__(self, url_params):
        """ This method has to return a valid url to attack """

        # Default language set to spanish for this app
        DEFAULT_LANGUAGE = 'es'
        url_params['lang'] = url_params.get('lang', DEFAULT_LANGUAGE)

        pars = url_params.copy()
        pars.update({'api_key': self.api_key})
        url = self.url.format(**pars)

        return url, pars


    def __response_treatment__(self, response):
        """ This function transform the response of the API into something lekta friendly """

        res = {}
        res['ForecastTemperature'] = self.__kelvin_to_celsius__(response['main']['temp'])
        print(response)
        res['ForecastDescriptor'] = response['weather'][0]['description']
        res['ForecastDatetime'] = 'Today'

        return res


    def current_weather(self, params):
        pars = params.copy()
        pars.update({'api_name': 'weather'})
        return self.__response_treatment__(self.__api_get__(*self.__url_builder__(pars)))


    def forecast(self, params):
        """ Forecast prediction options """
        pars = params.copy()
        pars.update({'api_name': 'forecast'})

        return self.__get_prediction__(self.__api_get__(*self.__url_builder__(pars)), pars)


    def __get_prediction__(self, data, url_params):
        day = url_params.get('day', 'all')
        mode = url_params.get('mode', 'both')
        helper = ForecastHelper(data)

        return helper.getPredictionsList(day, mode)

