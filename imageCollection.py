# stored = collection with all bands and geometry

from typing import Union
from authenticate import ee
from cloud_mask import maskS2clouds
def imageCollection(date):
    return ee.ImageCollection('COPERNICUS/S2_SR').filterDate(date[0], date[1])\
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))\
    .map(maskS2clouds)\
    .select(['TCI_R', 'TCI_G', 'TCI_B','QA60', 'B2', 'B3', 'B4', 'B8'])

# def getColl_Img(type : ee.Image | ee.ImageCollection, bands: list, geometry : ee.Geometry) -> Union[ee.Image , ee.ImageCollection]:
#     if isinstance(type, ee.ImageCollection):
#         return imageCollection.
    