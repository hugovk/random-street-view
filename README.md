random street view
==================

Command-line Python 3 script to get a number of Street View images from random locations in a given country.

Random (lat, lon) co-ordinates are generated from the country's border's bounding box, then checked to make sure they're within the actual borders. The corresponding Street View image downloaded. Often there is no imagery for the location, so if the size of the image matches that of the default "no imagery" thumbnail, it's deleted. Repeat until required number of images have been fetched.

You can see <a href="http://support.google.com/maps/bin/answer.py?hl=en&answer=68384">Street View coverage here</a>.

Prerequisites
-------------

 * Python 3.6+
 * Install Pillow and the Python Shapefile Library: `pip install pillow "pyshp>=2"` or `pip install -r requirements.txt`
 * Get the World Borders Dataset (e.g. TM_WORLD_BORDERS-0.3.shp) from http://thematicmapping.org/downloads/world_borders.php
 * Get a Google API key from https://developers.google.com/maps/documentation/streetview/ and put it in the .py file. The API is limited to 25,000 Street View image requests per 24 hours. You can check how much you've used at the <a href="https://code.google.com/apis/console/">console</a>.

Usage
-----

    usage: random_street_view.py [-h] country

    Get random Street View images from a given country

    positional arguments:
      country     ISO 3166-1 Alpha-3 Country Code

For example:

    python random_street_view.py GBR
