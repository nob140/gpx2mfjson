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
def gpx2mfjson2(inputfile, outputfile):
    gpx_file = open(inputfile, 'r')
    gpx = gpxpy.parse(gpx_file)

    features = []
    tracknum = 0

    for track in gpx.tracks:
        tracknum += 1

        # making lists without invalid points
        coordinates = []
        times = []
        lasttime = "0000-00-00"
        for segment in track.segments:
            for point in segment.points:
                if point.latitude is None or point.longitude is None or point.elevation is None or point.time is None:
                    #print('invalid point')
                    continue
                
                # convert time to timestr
                point.time = point.time.strftime('%Y-%m-%dT%H:%M:%S%z')
                # save only unique timestamp
                if lasttime != point.time:
                    coordinates.append([point.longitude, point.latitude, point.elevation])
                    times.append(point.time)
                lasttime = point.time

        feature = Feature(id= f"Route{tracknum}", geometry= LineString(coordinates= coordinates, precision=15), properties= {'datetimes':times})
        features.append(feature)

    gpx_file.close()

    json_file = open(outputfile, mode="w")
    json.dump(FeatureCollection(features), json_file, indent=2)
    json_file.close()

# converter function considering epsilon
# delete middle point of 3 same points by checking 'distance < epsilon'
# epsilon 0.00000001 is mm order
def gpx2mfjson3(inputfile, outputfile, epsilon):
    gpx_file = open(inputfile, 'r')
    gpx = gpxpy.parse(gpx_file)

    features = []
    tracknum = 0

    for track in gpx.tracks:
        tracknum += 1

        # making lists without invalid points
        points = []
        lasttime = "0000-00-00"
        for segment in track.segments:
            for point in segment.points:
                if point.latitude is None or point.longitude is None or point.elevation is None or point.time is None:
                    #print('invalid point')
                    continue

                # convert time to timestr
                point.time = point.time.strftime('%Y-%m-%dT%H:%M:%S%z')
                # save only unique timestamp
                if lasttime != point.time:
                    points.append(point)
                lasttime = point.time

        # check same 3 points
        for i in range(len(points)-2):
            # check horizontal distance (do not mind unit of measure)
            if abs(points[i].latitude - points[i+1].latitude) > epsilon:
                continue
            if abs(points[i+1].latitude - points[i+2].latitude) > epsilon:
                continue
            if abs(points[i].longitude - points[i+1].longitude) > epsilon:
                continue
            if abs(points[i+1].longitude - points[i+2].longitude) > epsilon:
                continue

            # unnecessary point flag
            points[i+1].time = None

        # feature by linestring geometry with only valid points
        coordinates = []
        times = []
        for point in points:
            if point.time is None:
                continue

            coordinates.append([point.longitude, point.latitude, point.elevation])
            times.append(point.time)
    
        feature = Feature(id= f"Route{tracknum}", geometry= LineString(coordinates= coordinates, precision=15), properties= {'datetimes':times})
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
        gpx2mfjson2(inputfile, arguments[2])
    else:
        gpx2mfjson3(inputfile, arguments[2], float(arguments[3]))

    print('process finished successfully.')
