# GPX2MovingFeaturesJSON
Converter from GPX Track to OGC Moving Features JSON (Trajectory encoding)

## Requirements
- pip install geojson
- pip install gpxpy

## Usage
- python.exe GPX2MovingFeaturesJSON.py input.GPX output.json

- python.exe GPX2MovingFeaturesJSON.py input.GPX output.json 0.0000001(epsilon for checking duplicated points)
