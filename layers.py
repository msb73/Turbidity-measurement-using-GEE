from authenticate import ee 
import folium
from imageCollection import imageCollection
from cloud_mask import maskS2clouds
def mM(image, ndwi_image) -> dict:
    #imc.getInfo()['bands'][0]['data_type']['min']
    return image.reduceRegion(
        reducer =  ee.Reducer.minMax(), 
        geometry =  ndwi_image.geometry(),
        bestEffort = True,
        scale =  10).getInfo()

def addRasterLayers(image : ee.Image, map: folium.map, name : str , visParams : dict):
        folium.raster_layers.TileLayer(
        tiles = image.getMapId(visParams)['tile_fetcher'].url_format,
        attr = 'Google Earth Engine',
        name = name,
        overlay = True,
        control = True
        ).add_to(map)
    
# def rgb(collection, map) ->  None:
#     image = collection.mean()
#     # minMax = mM(image)
#     visParams = {'min':0, 'max':1, 
#             #  'palette':['225ea8','41b6c4','a1dab4','034B48']
#              }
#     addRasterLayers(image, map, 'RGB', visParams)
#     return image

def ndwi(collection, geometry):

    return collection.select(['B3', 'B8'])\
        .mean()\
        .clip(geometry)\
        .normalizedDifference(['B3', 'B8'])\
        .rename('NDWI').gte(0.0)

def ndti(date, map, name):
    #Mapping function for ndti band collection
    def ndiff(image):
        return image.updateMask(ndwi_image)
    dic = {
        'Khadakwasla' : ee.Geometry.Polygon(
        [[[73.664, 18.398],
          [73.667, 18.394],
          [73.667, 18.389],
          [73.694, 18.385],
          [73.713, 18.390],
          [73.723, 18.400],
          [73.744, 18.402],
          [73.752, 18.412],
          [73.754, 18.424],
          [73.765, 18.421],
          [73.775, 18.439],
          [73.760, 18.448],
          [73.754, 18.443],
          [73.747, 18.439],
          [73.741, 18.433],
          [73.736, 18.430],
          [73.735, 18.423],
          [73.734, 18.419],
          [73.713, 18.412],
          [73.711, 18.406],
          [73.696, 18.405],
          [73.692, 18.399]]]),
    'Jambulwadi' : ee.Geometry.Polygon(
        [[[73.838, 18.432],
          [73.839, 18.432],
          [73.841, 18.433],
          [73.842, 18.433],
          [73.846, 18.437],
          [73.845, 18.440],
          [73.839, 18.439],
          [73.838, 18.436],
          [73.838, 18.433]]]),
    'muthariver' : ee.Geometry.Polygon(
        [[[73.791, 18.461],
          [73.794, 18.461],
          [73.809, 18.472],
          [73.812, 18.478],
          [73.820, 18.481],
          [73.823, 18.481],
          [73.826, 18.483],
          [73.832, 18.494],
          [73.836, 18.497],
          [73.837, 18.499],
          [73.838, 18.501],
          [73.837, 18.506],
          [73.842, 18.510],
          [73.845, 18.515],
          [73.848, 18.519],
          [73.852, 18.520],
          [73.854, 18.519],
          [73.862, 18.528],
          [73.861, 18.530],
          [73.863, 18.531],
          [73.865, 18.535],
          [73.869, 18.538],
          [73.880, 18.541],
          [73.886, 18.541],
          [73.894, 18.541],
          [73.901, 18.540],
          [73.906, 18.539],
          [73.907, 18.542],
          [73.902, 18.542],
          [73.898, 18.543],
          [73.893, 18.545],
          [73.887, 18.545],
          [73.880, 18.544],
          [73.874, 18.542],
          [73.869, 18.540],
          [73.866, 18.539],
          [73.862, 18.537],
          [73.860, 18.534],
          [73.858, 18.532],
          [73.857, 18.532],
          [73.856, 18.535],
          [73.856, 18.542],
          [73.856, 18.546],
          [73.858, 18.549],
          [73.860, 18.551],
          [73.865, 18.553],
          [73.864, 18.555],
          [73.862, 18.555],
          [73.857, 18.553],
          [73.855, 18.550],
          [73.852, 18.544],
          [73.852, 18.541],
          [73.852, 18.534],
          [73.854, 18.531],
          [73.858, 18.529],
          [73.858, 18.527],
          [73.856, 18.525],
          [73.853, 18.522],
          [73.847, 18.520],
          [73.842, 18.513],
          [73.835, 18.506]]])
}
    #Getting first image collection with all bands 
    collection = imageCollection(date, dic[name])
    #Creating ndti
    ndwi_image = ndwi(collection, dic[name])
    # Ndti image for layer
    collection = collection.select(['B3', 'B4']).map(ndiff)
    # applying geometry to ndti image
    ndtiImage = collection\
        .median()\
        .normalizedDifference(['B3', 'B4'])\
        .rename('NDTI')
    # ndtiImage = collection.mean()
    print('############################')
    minMax = mM(ndtiImage, ndwi_image)
    visParams = {'min':minMax['NDTI_min'], 'max':minMax['NDTI_max'], 
                 'bands' : ['NDTI'],
                 'opacity' : 1,
         'palette':['225ea8','41b6c4','a1dab4','034B48']
         }
    # visParams = {'min':0, 'max':1, 
    #              'bands' : ['NDTI'],
    #              'opacity' : 1,
    #      'palette':['blue','red']
    #      }
    # print('layers')
    # print(id(map))
    addRasterLayers(ndtiImage, map, 'NDTI', visParams)
    return collection\
        .toBands() # type: ignore
    # return collection.filterBounds(ndwi_geometry)

##################################TESTING CODE########################################
# def imageCollection():
#     return ee.ImageCollection('COPERNICUS/S2_SR').filterDate('2023-01-01', '2023-01-27')\
#     .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))\
#     .map(maskS2clouds)\
#     .select(['TCI_R', 'TCI_G', 'TCI_B','QA60', 'B2', 'B3', 'B4', 'B8'])

# collection = imageCollection()
# map = folium.Map()
# ndti(collection, map, 'Khadakwasla')
# ret = ndti(('2023-01-01', '2023-02-15'), folium.Map(),'Khadakwasla')