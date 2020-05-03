#! /usr/bin/python3

from parseKML import RotatedBoundingBox
from createKML import BBFactory

def test_end2end_demo_chunk():
    kml_file = './demo/demo_chunk.kml'

    rotBB = RotatedBoundingBox(kml_file)
    #print(rotBB)
    rotBB.extract_corners()
    limits = rotBB.extract_cable_limits()

    name = 'KML_name'
    bbf  = BBFactory(name)

    shape = bbf.from_strings(limits[0] + limits[1] + limits[2])
    print(shape)
    shape.to_file('output_end2end.kml')

# TODO:
# add walking through the directory tree and appending results from
# all input KML files to create a single KML output file
#

if __name__ == '__main__':
    test_end2end_demo_chunk()