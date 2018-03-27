import argparse
import os
import random
import shapefile  # pip install pyshp
import sys
import urllib
import getcolor
import json

# Optional, http://stackoverflow.com/a/1557906/724176
try:
    import timing
    assert(timing)  # avoid flake8 warning
except:
    pass

# Google Street View Image API
# 25,000 image requests per 24 hours
# See https://developers.google.com/maps/documentation/streetview/
API_KEY = "API KEY HERE"
GOOGLE_IMG_URL = ("http://maps.googleapis.com/maps/api/streetview?sensor=false&"
              "size=640x640&key=" + API_KEY)
GOOGLE_METADATA_URL = ("https://maps.googleapis.com/maps/api/streetview/metadata?"
              "size=640x640&key=" + API_KEY)

IMG_PREFIX = "img_"
IMG_SUFFIX = ".jpg"

parser = argparse.ArgumentParser(
    description="Get random Street View images from a given country",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '-n', '--images-wanted', type=int,
    default=10,
    help="Number of images wanted")
parser.add_argument('country',  help='ISO 3166-1 Alpha-3 Country Code')
parser.add_argument(
    '-hdg', '--heading',
    help="Heading in degrees: 0 and 360 north, 90 east, 180 south, 270 west")
parser.add_argument(
    '-p', '--pitch',
    help="Pitch in degrees: 0 is default, 90 straight up, -90 straight down")
args = parser.parse_args()


# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
# http://www.ariel.com.au/a/python-point-int-poly.html
def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

print "Loading borders"
shape_file = "TM_WORLD_BORDERS-0.3.shp"
if not os.path.exists(shape_file):
    print("Cannot find " + shape_file + ". Please download it from "
          "http://thematicmapping.org/downloads/world_borders.php "
          "and try again.")
    sys.exit()

sf = shapefile.Reader(shape_file)
shapes = sf.shapes()

print "Finding country"
for i, record in enumerate(sf.records()):
    if record[2] == args.country.upper():
        print record[2], record[4]
        print shapes[i].bbox
        min_lon = shapes[i].bbox[0]
        min_lat = shapes[i].bbox[1]
        max_lon = shapes[i].bbox[2]
        max_lat = shapes[i].bbox[3]
        borders = shapes[i].points
        break

print "Getting images"
imagery_hits = 0

if not os.path.exists(args.country):
    os.makedirs(args.country)

try:
    while(True):
        rand_lat = random.uniform(min_lat, max_lat)
        rand_lon = random.uniform(min_lon, max_lon)
        if point_inside_polygon(rand_lon, rand_lat, borders):
            lat_lon = str(rand_lat) + "," + str(rand_lon)
            outfile = os.path.join(
                args.country, IMG_PREFIX + lat_lon + IMG_SUFFIX)

            meta_url = GOOGLE_METADATA_URL + "&location=" + lat_lon
            img_url = GOOGLE_IMG_URL + "&location=" + lat_lon
            if args.heading:
                img_url += "&heading=" + args.heading
                meta_url += "&heading=" + args.heading
            if args.pitch:
                img_url += "&pitch=" + args.pitch
                meta_url += "&pitch=" + args.pitch
            try:
                meta_res = urllib.urlopen(meta_url)
                meta_body = meta_res.read()
                meta_json = json.loads(meta_body.decode("utf-8"))
                if 'status' in meta_json and meta_json['status'] == 'ZERO_RESULTS':
                    pass
                else:
                    urllib.urlretrieve(img_url, outfile)
            except KeyboardInterrupt:
                sys.exit("exit")
            except:
                pass
            if os.path.isfile(outfile):
                print lat_lon
                # get_color returns the main color of image
                color = getcolor.get_color(outfile)
                print color
                if color[0] == '#e3e2dd' or color[0] == "#e3e2de":
                    os.remove(outfile)
                else:
                    print "Got one!"
                    imagery_hits += 1
                    if imagery_hits == args.images_wanted:
                        break
except KeyboardInterrupt:
    print "Keyboard interrupt"

print "Downloaded:\t", imagery_hits

# End of file
