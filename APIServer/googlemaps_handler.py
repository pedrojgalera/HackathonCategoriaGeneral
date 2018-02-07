from api_handler import APIHandler


# HANDLER FOR GOOGLE MAPS GEOCODING API


class GoogleMapsAPI(APIHandler):

    def __init__(self):
        super().__init__(self.__class__.__name__)

    def __url_builder__(self, url_params):
        """ This function is where the url is formated specifically to attack this API """
        url = self.url.format(**url_params)

        return url, url_params


    def coordinates(self, params):
        pars = params.copy()
        pars.update({'api_name': 'geocode'})
        pars.update({'key': self.key_coor})

        response = self.__api_get__(*self.__url_builder__(pars))
        response = response.get('results', {})
        try:
            response = response[0]
        except:
            response = None
        response = response.get('geometry', {})
        response = response.get('location',{})
        latitude = response.get('lat', {})
        longitude = response.get('lng', {})

        res = {}
        if latitude and longitude:
            res = {
                'longitude': longitude,
                'latitude': latitude
            }

        return res


    def distance(self, params):
        pars = params.copy()
        pars.update({'api_name': 'distancematrix'})
        pars.update({'key': self.key_dist})
        if 'mode' not in pars:
            pars.update({'mode': 'walking'})

        res = self.__api_get__(*self.__url_builder__(pars))

        return res


