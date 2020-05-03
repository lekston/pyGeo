#!/usr/bin/python3

import sys
import os
import fnmatch
import csv

example_path="Chile_MRK/terreno 2 por km/vuelos/100_0042_Timestamp.MRK"

output_path="full_report_with_paths.txt"

class WriterClass(object):
    def __init__(self):
        labels = ['Lat', 'Lon', 'Alt', 'AccX', 'AccY', 'AccZ', 'Path']
        self.outfile = open(output_path, 'w')
        self.data_writer = csv.writer(self.outfile, delimiter='\t')
        self.data_writer.writerow(labels)

    def __del__(self):
        self.outfile.close()

    def dumpToFile(self, data, path):
        tidy = self.extractFields(data)
        # print(tidy)
        tidy.append(str(path))
        self.data_writer.writerow(tidy)

    def extractFields(self, data):
        lat = float(data[0].split(',')[0])
        lon = float(data[1].split(',')[0])
        alt = float(data[2].split(',')[0])
        AccX, AccY, AccZ = [float(i) for i in data[3].split(',')]
        return [lat, lon, alt, AccX, AccY, AccZ]

outWriter = WriterClass()

def extractColumns(root, item):
    path = root + '/' + item
    #limit = 3
    with open(path) as file:
        data_reader = csv.reader(file, delimiter='\t')
        for row in data_reader:
            #limit-=1
            #if not bool(limit):
            #    break
            #print(row[6:10])
            outWriter.dumpToFile(row[6:10], path)

def traverse(path, pattern):
    for root, dir, files in os.walk(path):
        if str(root) != ".":
            print(root)
        for item in fnmatch.filter(files, pattern):
            print("  > " + item)


def dummyAction(*argv):
    pass


def visit(path, pattern, action = dummyAction):
    for root, dir, files in os.walk(path):
        if str(root) != ".":
            print(root)
        for item in fnmatch.filter(files, pattern):
            print("  > " + item)
            action(root, item)


if __name__ == "__main__":
    try:
        path = "./Survey_Noviembre"
        if len(sys.argv) != 2:
            print("Usage: " + sys.argv[0] + " <path_to_dir>")
            print("\tWill use current dir.")
        else:
            path=sys.arg[1]

        visit(path, "*.MRK", action=extractColumns)
        sys.exit(0)
    except (RuntimeError, TypeError, NameError, Exception) as e:
        print("Caught: " + e + ". Exiting.")
    else:
        print("Unknown exception")