#!/usr/bin/env python3

import os
import json

def getCatsData(file):
    with open(file) as json_data:
        d = json.load(json_data)
    return d

class FoursquareHelper(object):
    def __init__(self,file=FILENAME):
        self.catsData = getCatsData(file)
        self.catsList = self.catsData['response']['categories']
        self.catsFlatList = self.flattenCats(self.catsList)

    def addEnrichedCategories(self,category,parentId=''):
        cats = []
        subcats = category.get('categories',[])
        cat = {
            'id' : category['id'],
            'name' : category['name'],
            'parentId' : parentId,
            'nsubcats' : len(subcats)
        }
        cats.append(cat)
        for category in subcats:
            cats.extend(self.addEnrichedCategories(category,cat['id']))
        return cats

    def flattenCats(self,categories):
        flatcats = []
        for category in categories:
            flatcats.extend(self.addEnrichedCategories(category))
        return flatcats

    def getCats(self,allcats=False):
        cats=self.catsFlatList
        if not allcats:
            cats = [cat for cat in cats if cat['parentId']=='']
        return cats

    def getCatsNames(self,flatMode=False):
        cats=self.catsList
        if flatMode:
            cats = self.catsFlatList
        catsNames = []
        for cat in cats:
            catsNames.append(cat['name'])
        return catsNames

    def getSubCats(self, parent=''):
        cats=self.catsFlatList
        return [cat for cat in cats if cat['parentId']==parent]

    def printCatSummary(self,cat,pref='',includeLeaves=False):
        subcats = self.getSubCats(parent=cat['id'])
        if includeLeaves or len(subcats)>0:
            print("{}{} (id {}): {} children".format(pref,cat['name'],cat['id'],cat['nsubcats']))
            for sc in subcats:
                self.printCatSummary(sc,pref+'  ')

    def catsSummaryByParent(self,parent='',includeLs=False):
        [self.printCatSummary(cat=c,includeLeaves=includeLs) for c in self.getSubCats(parent=parent)]
