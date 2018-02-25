import xml.etree.ElementTree as ET
from pyquery import PyQuery as pq
from lxml import etree
import urllib
import lxml

def printTree (tree,prefix=''):
    print(prefix+str(tree.tag))
    for child in tree:
        printTree(child,prefix+'   ')
    if tree.tag == 'story.date':
        print(tree)

tree = ET.parse('18073876.xml')
root = tree.getroot()
printTree(root)

with open('18073876.xml', 'r') as myfile:
    data=myfile.read().replace('\n', '').encode("utf-8")

#d = pq(data, parser='xml')
'''
for child in d.children():
    if (type(child) is lxml.etree._Element):
        print(child)
'''

pq1 = pq(data)
cont = 0
for item in pq1.children():
    cont +=1

import csv
'''
title = pq1('title').text()
subtitle = pq1('hl2').text()
with open('news.csv', 'w') as csvfile:
    fieldnames = ['title', 'subtitle']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'title': title, 'subtitle': subtitle})
    #writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    #writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
'''
