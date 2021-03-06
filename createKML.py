#! /usr/bin/python3

from lxml import etree
from pykml.factory import KML_ElementMaker as KML
#from pykml.factory import ATOM_ElementMaker as ATOM
#from pykml.factory import GX_ElementMaker as GX


class BBFactory(object):
    def __init__(self, name = 'default_name'):
        self.name = KML.name(name)
        self.geometry = None
        self.coords = ' '

    def from_points(self, coordinates):
        # create coordinates string
        coords = ' '
        for xyz in coordinates:
            coords += str(xyz[0]) + ',' \
                    + str(xyz[1]) + ',' \
                    + str(xyz[2]) + ' '
        return self.append_geometry(coords)

    def from_strings(self, coordinates):
        # create coordinates string
        coords = ' ' +  ' '.join(coordinates) + ' '
        return self.append_geometry(coords)

    def append_geometry(self, coords):
        line_string = KML.LineString( KML.coordinates(coords) )
        if self.geometry is None:
            self.geometry = KML.MultiGeometry(line_string)
        self.geometry.append(line_string)
        return self

    def __str__(self):
        place_mark = KML.Placemark(self.name, self.geometry)
        kml = KML.kml(place_mark)
        output = etree.tostring(kml, pretty_print=True)
        return output.decode('utf-8')

    def to_file(self, filename):
        string = self.__str__()
        with open('{}'.format(filename),'w') as f:
            f.write(string)


def test_from_points():
    name = 'KML_name'
    bbf  = BBFactory(name)
    coords = [[ 20.0, 50.0, 250],
              [ 20.0, 50.1, 250],
              [ 20.1, 50.1, 250],
              [ 20.1, 50.0, 250]]
    return bbf.from_points(coords).from_points(coords)


def test_from_strings():
    name = 'KML_name'
    bbf  = BBFactory(name)
    coords = [ '-70.42417428555072,-23.111384326733365,94.66195246706638',
               '-70.42347775711559,-23.10779964661056,88.0736153491157' ]
    return bbf.from_strings(coords)


if __name__ == '__main__':
    # bb = test_from_strings()
    bb = test_from_points()
    print(bb)
    with open('output.kml','w') as f:
        f.write(str(bb))
