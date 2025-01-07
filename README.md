# random street view

Command-line Python 3 script to get a number of Street View images from random locations
in a given country.

Random (lat, lon) co-ordinates are generated from the country's border's bounding box,
then checked to make sure they're within the actual borders. The corresponding Street
View image downloaded. Repeat until required number of images have been fetched.

## Prerequisites

- Python 3.9+
- Install Pillow and the Python Shapefile Library:
  `python -m pip install pillow "pyshp>=2"` or `pip install -r requirements.txt`
- Get the World Borders Dataset (e.g. TM_WORLD_BORDERS-0.3.shp) from
  http://thematicmapping.org/downloads/world_borders.php
- Get a Google API key from https://developers.google.com/maps/documentation/streetview/
  and put it in the .py file. The API is limited to 25,000 Street View image requests
  per 24 hours. You can check how much you've used at the
  <a href="https://code.google.com/apis/console/">console</a>.

## Usage

```
usage: random_street_view.py [-h] [-n IMAGES_WANTED] [-hdg HEADING] [-p PITCH]
                             country

Get random Street View images from a given country

positional arguments:
  country               ISO 3166-1 Alpha-3 Country Code

options:
  -h, --help            show this help message and exit
  -n IMAGES_WANTED, --images-wanted IMAGES_WANTED
                        Number of images wanted (default: 10)
  -hdg HEADING, --heading HEADING
                        Heading in degrees: 0 and 360 north, 90 east, 180
                        south, 270 west (default: None)
  -p PITCH, --pitch PITCH
                        Pitch in degrees: 0 is default, 90 straight up, -90
                        straight down (default: None)
```

For example:

```sh
python3 random_street_view.py GBR
```
