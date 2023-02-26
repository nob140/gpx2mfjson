# gpx2mfjson
Converter from GPX Track to OGC Moving Features JSON (Trajectory encoding)

## Requirements
- pip install geojson
- pip install gpxpy

## Usage
- python.exe gpx2mfjson.py input.GPX output.json

- python.exe gpx2mfjson.py input.GPX output.json 0.0000001(epsilon for checking duplicated points)

## Note
- multibyte characters will cause an error by the gpxpy parser. Please delete those characters manually before converting.