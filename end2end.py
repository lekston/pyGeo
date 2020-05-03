#! /usr/bin/python3

from parseKML import RotatedBoundingBox
from createKML import BBFactory
from ConCatAll import visit

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

bbox = None

def customAction(root, item):
    global bbox
    path = root + '/' + item

    if item != "mission.kml":
        rotBB = RotatedBoundingBox(path)
        # print(rotBB)
        # rotBB.extract_corners()
        limits = rotBB.extract_cable_limits(verbose=False)
        data = [item for sublist in limits for item in sublist]
        if bbox is not None:
            bbox.from_strings(data)


def test_all():
    name = 'KML_name'
    global bbox
    bbox = BBFactory(name)

    # test_end2end_demo_chunk()
    visit("KML_all", '*.kml', action=customAction)
    # print(bbox)
    with open('output_all.kml','w') as f:
        f.write(str(bbox))

if __name__ == '__main__':
    test_all()