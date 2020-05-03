#! /usr/bin/python3

from lxml import etree
from pykml import parser
from pykml.factory import KML_ElementMaker as KML

'''
pointXYZ = {
    "Lon": 0.0,
    "Lat": 0.0,
    "Alt": 0.0
}
'''


class PointList(object):
    def __init__(self, raw_points = None):
        self.pointsXYZ = []
        if raw_points is not None:
            self.parse_points(raw_points)

    def parse_points(self, raw_points):
        for point_str in raw_points:
            xyz = point_str.split(',')
            if len(xyz) == 3:
                self.pointsXYZ.append({
                    "Lon": xyz[0],
                    "Lat": xyz[1],
                    "Alt": xyz[2]
                })
        return self

    def get_points(self):
        return self.pointsXYZ


class RotatedBoundingBox(object):
    def __init__(self, file_path):
        self.tree = parser.parse(file_path)
        self.root = self.tree.getroot()
        self.parsed_points = []

    def __str__(self):
        out = ''
        try:
            out += 'Listing items:\n'
            for item in self.root.iter():
                out += '\t' + str(item.tag) + '\n'

            out += 'Listing dict:\n'
            out += '\t'+ str(self.root.Document.__dict__) + '\n'

            # A direct shortcut would be:
            # self.root.Document.Folder.Placemark.MultiGeometry.Linestring.__dict__
            # but this wound not explore the tree nor would it do error checking
            for entry in self.root.Document.Folder.getchildren():
                if 'Placemark' in entry.tag:
                    out += 'Found a placemark, exploring:\n'
                    out += '\t' + str(entry.__dict__) + '\n'
                    for geometry in entry:
                        if 'MultiGeometry' in geometry.tag:
                            out += '\t\t' + str(entry.__dict__) + '\n'
                        for item in geometry.getchildren():
                            out += '\t' + str(item.tag) + '\n'
        except AttributeError as e:
            print(e)
        return out

    def get_raw_points(self, lineString):
        for item in lineString.getchildren():
            if 'coordinates' in item.tag:
                raw_points = str(item).split(' ')
                yield raw_points

    def parse_line_string(self, lineString):
        for raw_points in self.get_raw_points(lineString):
            self.parsed_points += PointList(raw_points).get_points()
        return self.parsed_points


    def limiting_points(self, lineString):
        limit_list = []
        for raw_points in self.get_raw_points(lineString):
            # don't use last point as it can be an empty string
            limit_list += (raw_points[0], raw_points[-2])
        return limit_list

    def min_max_XY(self, points):
        lon = [pt['Lon'] for pt in points]
        lat = [pt['Lat'] for pt in points]
        # get indexes of min/max items
        min_lon_idx = min(range(len(lon)), key=lon.__getitem__)
        max_lon_idx = max(range(len(lon)), key=lon.__getitem__)
        min_lat_idx = min(range(len(lat)), key=lat.__getitem__)
        max_lat_idx = max(range(len(lat)), key=lat.__getitem__)
        return (min_lon_idx, max_lon_idx, min_lat_idx, max_lat_idx)

    def extract_corners(self):
        self.parsed_points = []
        for item in self.root.Document.Folder.Placemark.MultiGeometry.getchildren():
            if 'LineString' in item.tag:
                self.parse_line_string(item)

        if len(self.parsed_points) is not 0:
            indexes = self.min_max_XY(self.parsed_points)
            print("Indexes:\n\t" + str(indexes))
            corner_points = [self.parsed_points[i] for i in indexes]
            print("Corner points:")
            for pt in corner_points:
                print("\t" + str(pt))

    def extract_raw(self):
        for item in self.root.Document.Folder.Placemark.MultiGeometry.getchildren():
            if 'LineString' in item.tag:
                for raw_points in self.get_raw_points(item):
                    print(len(raw_points))

    def extract_cable_limits(self):
        limits = []
        for item in self.root.Document.Folder.Placemark.MultiGeometry.getchildren():
            if 'LineString' in item.tag:
                lim = self.limiting_points(item)
                limits.append( lim )
        for l in limits:
            print("Cable Limits:\n0:\t" + l[0] + "\n1:\t" + l[1])


kml_file = './demo/demo_chunk.kml'

rotBB = RotatedBoundingBox(kml_file)

#print(rotBB)

rotBB.extract_corners()
rotBB.extract_cable_limits()
