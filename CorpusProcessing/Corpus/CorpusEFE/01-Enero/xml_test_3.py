# import re
# text=open("18073876.xml").read()
# found=re.findall("<title>(.*)</title>",text)
# for title in found:
#     print(title)

path = "18073876.xml"

#path = "catalog.xml"

from xml.dom.minidom import parse, Node
xmltree=parse(path)
for node1 in xmltree.getElementsByTagName('body.content'):
    xml = node1.toxml()
    for p in xmltree.getElementsByTagName('p'):
        print(p)
    for node2 in node1.childNodes:
        print(node2)
        if node2.nodeType == Node.TEXT_NODE:
            print("Great ",node2.data)
