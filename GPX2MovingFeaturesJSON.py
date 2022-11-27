import sys
import os
import datetime

import json
from geojson import LineString, Feature, FeatureCollection
import gpxpy

def error(text):
	print(text)
	sys.exit()

# epsilon is not yet implemented now.
# same points should be deleted by checking 'distance < epsilon'
def GPX2MovingFeaturesJSON(inputfile, outputfile, epsilon):
    gpx_file = open(inputfile, 'r')
    gpx = gpxpy.parse(gpx_file)

    features = []
    num = 0

    for track in gpx.tracks:
        coordinates = []
        times = []
        num += 1

        for segment in track.segments:
            for point in segment.points:
                if point.latitude is None or point.longitude is None or point.elevation is None:
                    print('invalid point')
                    continue
                if point.time is None:
                    print('invalid timestamp')
                    continue

                coordinates.append([point.latitude, point.longitude, point.elevation])

                dtime = point.time
                times.append(dtime.strftime('%Y-%m-%dT%H:%M:%S%z'))
    
        feature = Feature(id='Route'+str(num), geometry= LineString(coordinates= coordinates, precision=15), properties= {'datetime':times})
        features.append(feature)

    gpx_file.close()

    json_file = open(outputfile, mode="w")
    json.dump(FeatureCollection(features), json_file, indent=2)
    json_file.close()


if __name__ == '__main__':
    usage = 'Usage: python {} INPUT_FILE OUTPUT_FILE EPSILON'.format(__file__)
    arguments = sys.argv
    if len(arguments) < 3:
        error(usage)
    if len(arguments) > 4:
        error(usage)

    inputfile = arguments[1]
    if os.path.exists(inputfile) == False:
        error(inputfile + " is not exist.")
    if os.path.isfile(inputfile) == False:
        error(inputfile + " is not file.")

    if len(arguments) == 3:
        epsilon = 0.0
    else:
        epsilon = float(arguments[3])

    GPX2MovingFeaturesJSON(inputfile, arguments[2], epsilon)
