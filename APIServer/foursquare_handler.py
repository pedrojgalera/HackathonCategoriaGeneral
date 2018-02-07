import requests, json
from api_handler import APIHandler
from googlemaps_handler import GoogleMapsAPI
from foursquare.foursquare_categories_helper import FoursquareCategoriesHelper
import datetime as dt

def stringToDate(timestamp_in_seconds):
    datetime_object = dt.datetime.fromtimestamp(timestamp_in_seconds)
    return datetime_object.strftime('%Y-%m-%d')

class FoursquareAPI(APIHandler):

    def __init__(self, temp=None):
        super().__init__(self.__class__.__name__)
        self.helper = FoursquareCategoriesHelper()
        if self.geo:
            self.GeoAPI = GoogleMapsAPI()

    def __url_builder__(self, url_params):
        """ This function is where the url is formated specifically to attack this API """
        pars = url_params.copy()
        pars.update({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'v': self.version
        })

        # Geocoding wrapper
        near_field = pars.get('near', None)
        if near_field and self.GeoAPI and 'll' not in pars:
             pars['address'] = near_field
             pars.pop('near')
             # Getting coordinates
             try:
                 coor = self.GeoAPI.coordinates(pars)
             except:
                 coor = {}

             # Passing geo param
             lat, lon = coor.get('latitude', None), coor.get('longitude', None)
             if lat and lon:
                pars['ll'] = str(lat) + ',' + str(lon)
                pars.pop('address')
             else:
                pars['near'] = near_field # Recovering "near" if something went wrong

        url = self.url.format(**pars)
        print(pars)
        return url, pars


    def categories_raw(self,params):
        return self.helper.catsData


    def categories_info(self,params):
        getAll = params.get('all',False)
        categories = {
            'categories_info': self.helper.getCats(allcats=getAll)
        }
        return categories


    def subcategories_info(self,params):
        parentId = params.get('parentId','')
        categories = {
            'categories_info': self.helper.getSubCats(parent=parentId)
        }
        return categories


    def categories_name(self,params):
        cats = self.categories_info(params)['categories_info']
        categories = {
            'categories_names': [cat['name'] for cat in cats]
        }
        return categories


    def subcategories_name(self,params):
        cats = self.subcategories_info(params)['categories_info']
        categories = {
            'categories_names': [cat['name'] for cat in cats]
        }
        return categories


    #def places_list(self,params): # TODO: URL
    #    listId='52a4c3d311d27e928435564b'
    #    list_url = 'https://api.foursquare.com/v2/lists/' + listId
    #    pars = self.defpars.copy()
    #    resp = requests.get(list_url, pars)
    #    data = json.loads(resp.text)
    #    return data


    def recommended_venues(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': 'explore',
            'param2': '',
            'limit': pars.get('limit', 10)
        })
        return self.__api_get__(*self.__url_builder__(pars))


    def tips(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': params.get('id','4b8bce70f964a52049ac32e3'), # Venue id has to be passed in the url.
            'param2': 'tips',
            'limit': pars.get('limit', 10)
        })
        r = self.__api_get__(*self.__url_builder__(pars))

        tipsList = []
        root = r.get('response')
        if root is not None:
            tips = root.get('tips')
            if tips is not None:
                items = tips.get('items',[])
                for item in items:
                    if item is not None:
                        t = {
                            'Tip' : {
                                'TipDate': stringToDate(item.get('createdAt')),
                                'TipText': item.get('text','nothing to declare'),
                                'TipLang': item.get('lang',params.get('lang','es'))
                            }
                        }
                        tipsList.append(t)

        res = { 'Tips' : tipsList }
        return res

    def details_all(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': params.get('id','4b8bce70f964a52049ac32e3'), # Venue id has to be passed in the url.
            'param2': '',
            'limit': pars.get('limit', 10)
        })
        return self.__api_get__(*self.__url_builder__(pars))

    def details(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': params.get('id','4b8bce70f964a52049ac32e3'), # Venue id has to be passed in the url.
            'param2': '',
            'limit': pars.get('limit', 10)
        })
        print(self.__url_builder__(pars)[0])
        r = self.__api_get__(*self.__url_builder__(pars))

        res = { 'Venue' : { } }
        root = r.get('response')
        if root is not None:
            venue = root.get('venue')
            if venue is not None:
                loc = venue.get('location')
                addr = 'Unknown'
                lat = 0
                lon = 0
                formattedAddr = 'Unknown'
                if loc is not None:
                    addr = loc.get('address','Unknown')
                    lat = loc.get('lat',0)
                    lon = loc.get('lng',0)
                    formattedAddr = ", ".join(loc.get('formattedAddress',[]))
                contact = venue.get('contact')
                phone = 'Unknown'
                formattedPhone = 'Unknown'
                if contact is not None:
                    phone = contact.get('phone','Unknown')
                    formattedPhone = contact.get('formattedPhone','Unknown')
                tipsList = []
                tips = venue.get('tips',{})
                if tips is not None:
                    groups = tips.get('groups',[])
                    for group in groups:
                        items = group.get('items',[])
                        for item in items:
                            if item is not None:
                                requestedLang = params.get('lang')
                                lang = item.get('lang',params.get('lang','es'))
                                includeItem = True
                                if requestedLang is not None and lang != requestedLang:
                                    includeItem = False
                                if includeItem:
                                    t = {
                                        'Tip' : {
                                            'TipDate': stringToDate(item.get('createdAt')),
                                            'TipText': item.get('text','nothing to declare'),
                                            'TipLang': item.get('lang',params.get('lang','es'))
                                        }
                                    }
                                    tipsList.append(t)
                prices = venue.get('price',[])
                #priceTier = sum(prices)/len(prices) if prices != [] else -1
                priceTier = prices[0] if prices != [] else -1
                ven = {
                    'VenueId': venue.get('id'),
                    'VenueName': venue.get('name'),
                    'Location': {
                        'LocationAddress' : formattedAddr,
                        'Geocoordinates' : {
                            'Lat' : lat,
                            'Lon' : lon
                        }
                    },
                    'Contact': {
                        'ContactPhone' : phone,
                        'ContactFormattedPhone' : formattedPhone
                    },
                    'VenueDescription' : venue.get('description'),
                    'Tips' : tipsList,
                    'PriceTier' : priceTier
                }
                ven.update(self.hours(params))
                v = {
                    'Venue' : ven
                }

                res = v
        return res

    def search(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': 'search',
            'param2': '',
            'limit': pars.get('limit', 10)
        })
        return self.__api_get__(*self.__url_builder__(pars))


    def hours_all(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': params.get('id','4b8bce70f964a52049ac32e3'), # Venue id has to be passed in the url.
            'param2': 'hours',
            'limit': pars.get('limit', 10)
        })
        return self.__api_get__(*self.__url_builder__(pars))

    def hours(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': params.get('id','4bcabe4268f976b0eafe5f83'),
            'param2': 'hours',
            'limit': pars.get('limit', 10)
        })
        r = self.__api_get__(*self.__url_builder__(pars))

        venues = []
        root = r.get('response')
        frames = []
        if root is not None:
            hours = root.get('hours')
            if hours is not None:
                timeframes = hours.get('timeframes',[])
                for timeframe in timeframes:
                    openDays = [ {
                        'OpeningDay' : day
                        }
                        for day in timeframe.get('days')]
                    openFrames = [ {
                        'OpeningFrame' : {
                            'OpeningStart' : frame.get('start'),
                            'OpeningEnd' : frame.get('end'),
                            }
                        }
                        for frame in timeframe.get('open')]
                    tf = {
                        'OpeningHours' : {
                            'OpeningDays' : openDays,
                            'OpeningFrames' : openFrames
                        }
                    }
                    frames.append(tf)
        oh = {
            'OpeningHoursList' : frames
        }
        return oh

    def menu(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': params.get('id','4b8bce70f964a52049ac32e3'), # Venue id has to be passed in the url.
            'param2': 'menu',
            'limit': pars.get('limit', 10)
        })
        return self.__api_get__(*self.__url_builder__(pars))

    def similar_all(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': params.get('id','4b8bce70f964a52049ac32e3'), # Venue id has to be passed in the url.
            'param2': 'similar',
            'limit': pars.get('limit', 10)
        })

        return self.__api_get__(*self.__url_builder__(pars))

    def similar(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': params.get('id','4b8bce70f964a52049ac32e3'), # Venue id has to be passed in the url.
            'param2': 'similar',
            'limit': pars.get('limit', 10)
        })

        r = self.__api_get__(*self.__url_builder__(pars))

        venues = []
        root = r.get('response')
        if root is not None:
            similarVenues = root.get('similarVenues')
            if similarVenues is not None:
                items = similarVenues.get('items',[])
                for venue in items:
                    if venue is not None:
                        loc = venue.get('location')
                        addr = 'Unknown'
                        lat = 0
                        lon = 0
                        formattedAddr = 'Unknown'
                        if loc is not None:
                            addr = loc.get('address','Unknown')
                            lat = loc.get('lat',0)
                            lon = loc.get('lng',0)
                            formattedAddr = ", ".join(loc.get('formattedAddress',[]))
                        contact = venue.get('contact')
                        phone = 'Unknown'
                        formattedPhone = 'Unknown'
                        if contact is not None:
                            phone = contact.get('phone','Unknown')
                            formattedPhone = contact.get('formattedPhone','Unknown')
                        origins = pars.get('ll')
                        destinations = str(lat) + ',' + str(lon)
                        pars.update({
                            'origins': origins,
                            'destinations': destinations
                        })
                        aux = {}
                        distances = self.GeoAPI.distance(pars)
                        print(distances)
                        rows = distances.get('rows', [])
                        if rows:
                            aux = rows[0]
                            elements = aux.get('elements', [])
                            if elements:
                                aux = elements[0]


                        v = {
                            'RecommendedVenue' : {
                                'VenueId': venue.get('id'),
                                'VenueName': venue.get('name'),
                                'Location': {
                                    'LocationAddress' : formattedAddr,
                                    'Geocoordinates' : {
                                        'Lat' : lat,
                                        'Lon' : lon
                                    }
                                },
                                'Contact': {
                                    'ContactPhone' : phone,
                                    'ContactFormattedPhone' : formattedPhone
                                },
                                'VenueDuration': {
                                    'VenueDurationText': aux.get('duration', {}).get('text', 'defaulttext'),
                                    'VenueDurationValue':   aux.get('duration', {}).get('value', 'defaultvalue')
                                },
                                'VenueDistance': {
                                    'VenueDistanceText': aux.get('distance', {}).get('text', 'defaulttext'),
                                    'VenueDistanceValue':   aux.get('distance', {}).get('value', 'defaultvalue')
                                }
                            }
                        }
                        venues.append(v)

        res = { 'RecommendedVenues' : venues }
        return res

    def events(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': params.get('id','4b8bce70f964a52049ac32e3'), # Venue id has to be passed in the url.
            'param2': 'events',
            'limit': pars.get('limit', 10)
        })
        return self.__api_get__(*self.__url_builder__(pars))


    def nextvenues(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1': pars.get('id','4af1b973f964a52083e221e3'), # Venue id has to be passed in the url.
            'param2': 'nextvenues',
            'limit': pars.get('limit', 10)
        })
        r = self.__api_get__(*self.__url_builder__(pars))

        venues = []
        root = r.get('response')
        if root is not None:
            nextvenues = root.get('nextVenues')
            if nextvenues is not None:
                items = nextvenues.get('items',[])
                for venue in items:
                    if venue is not None:
                        loc = venue.get('location')
                        addr = 'Unknown'
                        lat = 0
                        lon = 0
                        formattedAddr = 'Unknown'
                        if loc is not None:
                            addr = loc.get('address','Unknown')
                            lat = loc.get('lat',0)
                            lon = loc.get('lng',0)
                            formattedAddr = ", ".join(loc.get('formattedAddress',[]))
                        contact = venue.get('contact')
                        phone = 'Unknown'
                        formattedPhone = 'Unknown'
                        if contact is not None:
                            phone = contact.get('phone','Unknown')
                            formattedPhone = contact.get('formattedPhone','Unknown')
                        origins = pars.get('ll')
                        destinations = str(lat) + ',' + str(lon)
                        pars.update({
                            'origins': origins,
                            'destinations': destinations
                        })
                        aux = {}
                        distances = self.GeoAPI.distance(pars)
                        print(distances)
                        rows = distances.get('rows', [])
                        if rows:
                            aux = rows[0]
                            elements = aux.get('elements', [])
                            if elements:
                                aux = elements[0]


                        v = {
                            'RecommendedVenue' : {
                                'VenueId': venue.get('id'),
                                'VenueName': venue.get('name'),
                                'Location': {
                                    'LocationAddress' : formattedAddr,
                                    'Geocoordinates' : {
                                        'Lat' : lat,
                                        'Lon' : lon
                                    }
                                },
                                'Contact': {
                                    'ContactPhone' : phone,
                                    'ContactFormattedPhone' : formattedPhone
                                },
                                'VenueDuration': {
                                    'VenueDurationText': aux.get('duration', {}).get('text', 'defaulttext'),
                                    'VenueDurationValue':   aux.get('duration', {}).get('value', 'defaultvalue')
                                },
                                'VenueDistance': {
                                    'VenueDistanceText': aux.get('distance', {}).get('text', 'defaulttext'),
                                    'VenueDistanceValue':   aux.get('distance', {}).get('value', 'defaultvalue')
                                }
                            }
                        }
                        venues.append(v)

        res = { 'RecommendedVenues' : venues }
        return res

    def suggestions(self, params):
        pars = params.copy()
        pars.update({
            'endpoint': 'venues',
            'param1':  'explore',
            'param2': '',
            'limit': pars.get('limit', 10)
        })
        r = self.__api_get__(*self.__url_builder__(pars))

        venues = []
        root = r.get('response')
        if root is not None:
            groups = root.get('groups')
            if groups is not None:
                for group in groups:
                    items = group.get('items',[])
                    for item in items:
                        venue = item.get('venue')
                        if venue is not None:
                            loc = venue.get('location')
                            addr = 'Unknown'
                            lat = 0
                            lon = 0
                            formattedAddr = 'Unknown'
                            if loc is not None:
                                addr = loc.get('address','Unknown')
                                lat = loc.get('lat',0)
                                lon = loc.get('lng',0)
                                formattedAddr = ", ".join(loc.get('formattedAddress',[]))
                            contact = venue.get('contact')
                            phone = 'Unknown'
                            formattedPhone = 'Unknown'
                            if contact is not None:
                                phone = contact.get('phone','Unknown')
                                formattedPhone = contact.get('formattedPhone','Unknown')
                            prices = venue.get('price',{})
                            #priceTier = sum(prices)/len(prices) if prices != [] else -1
                            priceTier = prices.get('tier',-1)
                            v = {
                                'RecommendedVenue' : {
                                    'VenueId': venue.get('id'),
                                    'VenueName': venue.get('name'),
                                    'Location': {
                                        'LocationAddress' : formattedAddr,
                                        'Geocoordinates' : {
                                            'Lat' : lat,
                                            'Lon' : lon
                                        }
                                    },
                                    'Contact': {
                                        'ContactPhone' : phone,
                                        'ContactFormattedPhone' : formattedPhone
                                    },
                                    'PriceTier': priceTier
                                }
                            }
                            venues.append(v)

        res = { 'RecommendedVenues' : venues }
        return res


    def specificSuggestions(self, params, catId=None):
        pars = params
        cat = pars.get('categoryId')
        if cat is None and catId is not None:
            pars.update( { 'categoryId': catId })
        return self.suggestions(pars)


    def historicSites(self, params):
        return self.specificSuggestions(params,'4deefb944765f83613cdba6e')


    def restaurants(self, params):
        return self.specificSuggestions(params,'4d4b7105d754a06374d81259')


    def museums(self, params):
        return self.specificSuggestions(params,'4bf58dd8d48988d181941735')


    def sports(self, params):
        return self.specificSuggestions(params,'4f4528bc4b90abdf24c9de85')


    def parks(self, params):
        return self.specificSuggestions(params,'4bf58dd8d48988d163941735')


    def naturepreserve(self, params):
        return self.specificSuggestions(params,'52e81612bcbc57f1066b7a13')


    def nationalparks(self, params):
        return self.specificSuggestions(params,'52e81612bcbc57f1066b7a21')


    def specificQuery(self, params, query=None, catId=None):
        pars = params
        q = pars.get('query')
        if q is None and query is not None:
            pars.update({'query': query})
        if catId is not None:
            suggestions = self.specificSuggestions(pars,catId)
        else:
            suggestions = self.generalSuggestions(pars)
        return suggestions


    def nature(self, params):
        return self.specificQuery(params, 'nature')
