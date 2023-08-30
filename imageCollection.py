# stored = collection with all bands and geometry

from typing import Union
from authenticate import ee
from cloud_mask import maskS2clouds
def imageCollection(date, geometry):
    collection = ee.ImageCollection('COPERNICUS/S2_SR')\
        .filterDate(date[0], date[1])\
        .filterBounds(geometry)\
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',40))\
        .map(maskS2clouds)\
        .select(['TCI_R', 'TCI_G', 'TCI_B','QA60', 'B3', 'B4', 'B8'])
    return collection

# def getColl_Img(type : ee.Image | ee.ImageCollection, bands: list, geometry : ee.Geometry) -> Union[ee.Image , ee.ImageCollection]:
#     if isinstance(type, ee.ImageCollection):
#         return imageCollection.
    