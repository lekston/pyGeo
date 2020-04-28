from lxml import etree
from pykml import parser
from pykml.factory import KML_ElementMaker as KML

kml_file = './demo_chunk.kml'

tree = parser.parse(kml_file)

root = tree.getroot()

for item in root.iter():
    print(item.tag)

# root.Document.__dict__

try:
    for ch in root.Document.Folder.getchildren():
        if 'Placemark' in ch.tag:
            print('Found a placemark, exploring:')
            print(ch.__dict__)
            print(ch.MultiGeometry.__dict__)
    for item in root.Document.Folder.Placemark.MultiGeometry.getchildren():
        print(item.tag)
except AttributeError as e:
    print(e)


pointXYZ = {
    "Lon": 0.0,
    "Lat": 0.0,
    "Alt": 0.0
}

def toUnparsedPoints(lineString):
    for item in lineString.getchildren():
        if 'coordinates' in item.tag:
            unparsed_points = str(item).split(' ')
            yield unparsed_points

def toParsedPoints(unparsed_points):
    parsed_points = []
    for point_str in unparsed_points:
        xyz = point_str.split(',')
        if len(xyz) == 3:
            parsed_points.append({
                "Lon": xyz[0],
                "Lat": xyz[1],
                "Alt": xyz[2]
            })
    return parsed_points

def limitsOnly(lineString):
    limitList = []
    for unparsed_points in toUnparsedPoints(lineString):
        print(len(unparsed_points))
        # don't use last point as it is
        limitList += (unparsed_points[0], unparsed_points[-2])
    return limitList

def parseLineString(lineString):
    parsed_points = []
    for unparsed_points in toUnparsedPoints(lineString):
        parsed_points += toParsedPoints(unparsed_points)
    return parsed_points

def MinMaxXY(points):
    lon = [pt['Lon'] for pt in points]
    lat = [pt['Lat'] for pt in points]
    minLon = min(lon)
    maxLon = max(lon)
    minLat = min(lat)
    maxLat = max(lat)
    return (minLon, maxLon, minLat, maxLat)


for item in root.Document.Folder.Placemark.MultiGeometry.getchildren():
    if 'LineString' in item.tag:
        points = parseLineString(item)
        print(MinMaxXY(points))

for item in root.Document.Folder.Placemark.MultiGeometry.getchildren():
    if 'LineString' in item.tag:
        for unparsed_points in toUnparsedPoints(item):
            print(len(unparsed_points))

for item in root.Document.Folder.Placemark.MultiGeometry.getchildren():
    if 'LineString' in item.tag:
        lim = limitsOnly(item)
        print(lim)