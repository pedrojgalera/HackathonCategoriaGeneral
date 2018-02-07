#!/usr/bin/env python3

import os
import json
import datetime
import pytemperature
from math import floor

FILENAME = os.path.dirname(os.path.abspath(__file__))+'/forecast_example.json'

def getForecastData(file=FILENAME):
    with open(file) as json_data:
        d = json.load(json_data)
    return d

class ForecastHelper(object):
    """
    Helper class for Weather API forecast calls.
    It contains useful methods to make Weather API
    cleaner and more powerful
    It should receive the original call from Weather API
    Then it performs whatever processing the caller intends to do,
    by simply calling helper and sending back the target response object,
    before the handler sends it back to http server
    """

    DAYMINTIME = '00:00:00'
    DAYMAXTIME = '23:59:59'
    DAYTIMEINTERVAL = [DAYMINTIME,DAYMAXTIME]

    def __init__(self,data=''):
        """
        Class builder
        Could receive the json coming from call performed by Weather API
        Otherwise, works with temporary example local file cont. forecast call
        """
        self.forecastData = getForecastData() if data == '' else data

    def getCityDetails(self):
        """
        Details about the city where we focus the call
        """
        return self.forecastData['city']

    def getCount(self):
        """
        Number of total time frames included in the raw call
        """
        return self.forecastData['cnt']

    def getRawPredictionsList(self):
        """
        List of predictions in the raw call
        """
        return self.forecastData['list']

    def getDayRange(self,day,mode='both'):
        """
        List with the two datetimes when the day passed as a parameter
        starts and ends (from 0 to 23:59)
        """
        if mode == 'both' or mode == '':
            interval = [" ".join([day,frame]) for frame in ForecastHelper.DAYTIMEINTERVAL]
        elif mode == 'left':
            interval = [" ".join([day,ForecastHelper.DAYTIMEINTERVAL[0]])]
        elif mode == 'right':
            interval = [" ".join([day,ForecastHelper.DAYTIMEINTERVAL[1]])]
        else:
            interval = []
        return interval

    def dateInRange(self,date,dateRange=[],mode='both'):
        """
        Indicates if date is inside the interval given by the range included
        in the list dateRange.
        If no range is passed, it returns True.
        Otherwise, it can receive a lower limit,
        an upper limit or both
        """
        if len(dateRange) >= 2:
            isInRange = date >= dateRange[0] and date <= dateRange[1]
        elif len(dateRange) == 1:
            if (mode=='right'):
                isInRange = date <= dateRange[0]
            else:
                isInRange = date >= dateRange[0]
        else:
            isInRange = True
        return isInRange

    def getPredictionsList(self,day='all',mode='both'):
        """
        Predictions List for each interval included in the query
        If day='all', all the predictions in the raw call are included
        in the response.
        Otherwise, the predictions for the present day ('') or another
        given day ('yyyy-mm-dd') are returned.
        """
        predictions = self.getRawPredictionsList()
        if day == 'all':
            validInterval = []
        else:
            day = day if day != 'today' else ''
            refDay = day    if day != '' \
                            else (datetime.datetime.now().isoformat()[:10])
            validInterval = self.getDayRange(refDay,mode)
        preds = \
            { 'ForecastList' : [
                {
                    'ForecastElement' : {
                        'ForecastTemperature'  : str(floor(pytemperature.k2c(p['main']['temp']))),
                        'ForecastDescriptor'  : p['weather'][0]['description'],
                        'ForecastDescriptorId'  : p['weather'][0]['id'],
                        'ForecastDt'    : p['dt_txt']
                    }
                }
                for p in predictions
                if self.dateInRange(p['dt_txt'],validInterval,mode)
            ] }
        return preds
