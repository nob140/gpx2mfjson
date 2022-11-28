import sys
import os
import datetime

import json
from geojson import LineString, Feature, FeatureCollection
import gpxpy

def error(text):
	print(text)
	sys.exit()

# simple converter function from GPX to OGC Moving Features JSON
def GPX2MovingFeaturesJSON(inputfile, outputfile):
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

# converter function considering epsilon
# delete middle point of 3 same points by checking 'distance < epsilon'
def GPX2MovingFeaturesJSON2(inputfile, outputfile, epsilon):
    gpx_file = open(inputfile, 'r')
    gpx = gpxpy.parse(gpx_file)

    features = []
    tracknum = 0

    for track in gpx.tracks:
        tracknum += 1

        # making lists without invalid points
        lats, lons, elevs, times = [], [], [], []
        for segment in track.segments:
            for point in segment.points:
                if point.latitude is None or point.longitude is None or point.elevation is None or point.time is None:
                    #print('invalid point')
                    continue
                lats.append(point.latitude)
                lons.append(point.longitude)
                elevs.append(point.elevation)
                times.append(point.time)

        # check same 3 points
        for index in range(len(lats)-2):
            # check horizontal distance
            if abs(lats[index] - lats[index+1]) > epsilon or abs(lats[index+1] - lats[index+2]) > epsilon:
                continue
            if abs(lons[index] - lons[index+1]) > epsilon or abs(lons[index+1] - lons[index+2]) > epsilon:
                continue

            # unnecessary point flag
            times[index+1] = None
        
        # feature by linestring geometry with only valid points
        coordinates = []
        timestrs = []
        for index in range(len(lats)):
            if times[index] is None:
                continue

            coordinates.append([lats[index], lons[index], elevs[index]])
            timestrs.append(times[index].strftime('%Y-%m-%dT%H:%M:%S%z'))
    
        feature = Feature(id='Route'+str(tracknum), geometry= LineString(coordinates= coordinates, precision=15), properties= {'datetime':timestrs})
        features.append(feature)

    gpx_file.close()

    json_file = open(outputfile, mode="w")
    json.dump(FeatureCollection(features), json_file, indent=2)
    json_file.close()


if __name__ == '__main__':
    usage = 'Usage: python {} INPUT_FILE OUTPUT_FILE [EPSILON]'.format(__file__)
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
        GPX2MovingFeaturesJSON(inputfile, arguments[2])
    else:
        GPX2MovingFeaturesJSON2(inputfile, arguments[2], float(arguments[3]))
