"""
Getting a random point inside a country based on its name.
In this solution, the shapefile with countries was used.
"""

# imports
import re
import random
import shapefile
from shapely.geometry import shape, Point


# function that takes a shapefile location and a country name as inputs
def random_point_in_country(shp_location, country_name):
    shapes = shapefile.Reader(shp_location)  # reading shapefile with pyshp library
    country = [s for s in shapes.records() if country_name in s][0]  # getting feature(s) that match the country name
    country_id = int(re.findall(r'\d+', str(country))[0])  # getting feature(s)'s id of that match

    shapeRecs = shapes.shapeRecords()
    feature = shapeRecs[country_id].shape.__geo_interface__

    shp_geom = shape(feature)

    minx, miny, maxx, maxy = shp_geom.bounds
    while True:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if shp_geom.contains(p):
            print(p.y, p.x)
            return p.y, p.x


random_point_in_country("../test_file/shape_file/World_Countries.shp", "Ukraine")
