from authenticate import ee
import folium
# from cloud_mask import maskS2clouds
dataset = ee.ImageCollection('COPERNICUS/S2_SR').filterDate('2023-02-01', '2023-02-15').select(['B4', 'B3', 'B2']).median()
    # .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))\
    # .map(maskS2clouds)\

visParams = {'min':1125.61, 'max':6026.89, 
            #  'palette':['225ea8','41b6c4','a1dab4','034B48']
             }

# print(modisndvi)

# dem = ee.Image('USGS/SRTMGL1_003')
# vis_params = {
#   'min': 0,
#   'max': 4000,
#   'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}
# elev = dem.sample(xy, 30).first().get('elevation').getInfo()
# print('Mount Everest elevation (m):', elev)
def gee(map):
    map_id_dict = dataset.getMapId(visParams)
    folium.raster_layers.TileLayer(
        tiles = map_id_dict['tile_fetcher'].url_format,
        attr = 'Google Earth Engine',
        name = 'RGB',
        overlay = True,
        control = True
        ).add_to(map)
