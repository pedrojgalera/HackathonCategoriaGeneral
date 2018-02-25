import xml.etree.ElementTree as ET

def printTree (tree,prefix=''):
    print(prefix+str(tree.tag))
    for child in tree:
        printTree(child,prefix+'   ')

tree = ET.parse('18073876.xml')
root = tree.getroot()
#printTree(root)
#
print(tree)

for E in tree.findall('*'):
    print(E)

value = ET.find('title')
