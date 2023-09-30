# gpx2mfjson
Converter from GPX Track to OGC Moving Features JSON (Trajectory encoding)

## Requirements
This script uses [geojson](https://pypi.org/project/geojson/) and [gpxpy](https://pypi.org/project/gpxpy/).
```
pip install geojson
pip install gpxpy
```

## Usage
```
python.exe gpx2mfjson.py input.GPX output.json [EPSILON]
```
EPSILON: for checking duplicated points (i.e. 0.000001)


## Note
- multibyte characters will cause an error by the gpxpy parser. Please delete those characters manually before converting.
