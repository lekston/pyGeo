#! /usr/bin/python3

from lxml import etree
from pykml.factory import KML_ElementMaker as KML
#from pykml.factory import ATOM_ElementMaker as ATOM
#from pykml.factory import GX_ElementMaker as GX


class BBFactory(object):
    def __init__(self, name = 'default_name'):
        self.name = name
        self.pms = []
        self.coords = ' '
        self.count = 0

    def from_points(self, coordinates):
        # create coordinates string
        coords = ' '
        for xyz in coordinates:
            coords += str(xyz[0]) + ',' \
                    + str(xyz[1]) + ',' \
                    + str(xyz[2]) + ' '
        return self.append_place(coords)

    def from_strings(self, coordinates):
        # create coordinates string
        coords = ' ' +  ' '.join(coordinates) + ' '
        return self.append_place(coords)

    def append_place(self, coords):
        self.count += 1
        name = KML.name(self.name + "_{:04d}".format(self.count))
        geometry = KML.MultiGeometry( KML.LineString( KML.coordinates(coords) ) )
        self.pms.append( KML.Placemark(name , geometry) )
        return self

    def __str__(self):
        kml = KML.kml()
        for pm in self.pms:
            kml.append(pm)
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
