from authenticate import ee
from gee import imageCollection
geometry = ee.Geometry.Point([73.50502848893966,18.09751560212352])

# imageCollection = imageCollection.select(['B2', 'B3', 'B4'])
imageCollection = ee.ImageCollection('COPERNICUS/S2_SR').filterDate('2023-02-01', '2023-02-15').select(['B2', 'B3', 'B4']).filterBounds(geometry=geometry)
# def conditional(image, list):
#     return ee.List(list).add(image.reduceRegion(ee.Reducer.toList(), geometry, 10))

# ls = imageCollection.iterate(conditional, ee.List([]))
# print(ls.getInfo())
tobands_image = imageCollection.toBands()
# def get_ndti(image):
reduced = tobands_image.reduceRegion(
    reducer =  ee.Reducer.first(), 
    geometry =  geometry,
    bestEffort = True,
    scale =  10).getInfo()
# dic = {j[:8] : [] for j in list(reduced.keys())[::3]}
# count = 0
# for i in reduced:
#     dic[i[:8]].append(reduced[i])
# print(reduced.getInfo())
