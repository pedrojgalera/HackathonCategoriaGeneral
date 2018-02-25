

import json
import requests
import inspect

client_id='SNJDLNR0H0XBGHEGQQQ5HUSDIFYIEVBAYOE0HJBBMK3GFVBK',
client_secret='2KQG0QO5T24D4PNC4OCNAXJHQGAO1XVCH0RQCRCXNM3AWINF',
api_key='AIzaSyBRHPV3lLLKK6TBpaiVymGWPdYhtN2Tw00'

exclusions = ['call_method', 'params_treatment', 'getFunctionsMap']

class GoogleAPI(object):

    def __init__(self, temp=None, client=client_id, secret=client_secret, key=api_key):
        self.client = client
        self.secret = secret
        self.key = key
        self.version='20180112'
        self.defpars = {
            'key' : self.key
        }

    def getFunctionsMap(self):
        methodNames = \
            [
                x[0] for x in \
                inspect.getmembers(
                    self,
                    predicate=(lambda x: inspect.ismethod(x) and not x.__name__.startswith('__')))
            ]
        methods = list(set(methodNames)-set(exclusions))
        mymap = {}
        for method in methods:
            mymap.update({ method : self.__class__ })
        return mymap

    def call_method(self, url_params):
        params = self.params_treatment(url_params)
        function = params.pop('function')
        return getattr(self, function)(params)

    def params_treatment(self, params):
        return {key: value[0] for key, value in params.items()}

    def timezone(self,params):
        url = 'https://maps.googleapis.com/maps/api/timezone/json?location={ll}&timestamp={ts}&key={key}'.format(ll=params.get('location','37.3753501,-6.0250983'),ts=params.get('timestamp','1331161200'),key=params.get('key','AIzaSyBRHPV3lLLKK6TBpaiVymGWPdYhtN2Tw00'))
        pars = self.defpars.copy()
        pars.update({'limit':10})
        pars.update(**params)
        resp = requests.get(url, pars)
        data = json.loads(resp.text)
        return data
