from weather_handler import WeatherAPI
from foursquare_handler import FoursquareAPI
from google_handler import GoogleAPI
from googlemaps_handler import GoogleMapsAPI

functions_map = dict()

functions_map.update(WeatherAPI().__get_functions_map__())
functions_map.update(FoursquareAPI().__get_functions_map__())
functions_map.update(GoogleMapsAPI().__get_functions_map__())
functions_map.update(GoogleAPI().getFunctionsMap())
print(functions_map)

