#!/usr/bin/env python3

import json

lines = []
q = '\''

def sc(s):
    return (q + s + q)

def formatCat(cat):
    catSemObj = '( FsVenueCategory_id : ' + sc(cat['id']) + ', FsVenueCategory_name : ' + sc(cat['name']) + ', FsVenueCategory_pluralName : ' + sc(cat['pluralName']) + ', FsVenueCategory_shortName : ' + sc(cat['pluralName']) +  ' )'
    return catSemObj

def buildFsCatLine(cat):
    catLine = '("' + cat['name'] + '", lexFsVenueCategory, ' + formatCat(cat) + ')\n';
    return catLine

def showCat(cat,pref=''):
    print(pref,cat['name'])
    lines.append(buildFsCatLine(cat))
    subno = 1
    for subcategory in cat['categories']:
        subno += showCat(subcategory,pref+'   ')
    return subno

def showCategoriesTree():
    catno = 0
    for category in d['response']['categories']:
        catno += showCat(category)
    print(catno)

def generateLektaCats():
    fh = open("FsVenueCategories.lkt","w")
    fh.writelines(lines)
    fh.close()
