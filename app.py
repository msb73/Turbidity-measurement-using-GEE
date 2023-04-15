from flask import Flask, request
import folium
from authenticate import ee
from imageCollection import imageCollection
from basemap import basemaps
import layers


# def authenticate():
#     ee.Authenticate()
#     ee.Initialize()
# authenticate()
app = Flask(__name__)
collection = ee.ImageCollection
@app.route("/", methods = ['POST', 'GET'])
def fullscreen():
    my_map = folium.Map(location=[20, 0], zoom_start=3, height=1000)
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    # my_map.add_child(folium.LayerControl())
    if request.method == 'POST':
        print('post')
        return my_map.get_root().render()
    date = ('2023-01-01', '2023-02-15')
    location = 'Khadakwasla'
    # locations = {
    #     'Khadakwasla' : ([20, 0], ee.Geometry.Point([[73.73801385248593, 18.412317318279012]]), 3),
    #     'Mula mutha' : ([20, 0], ee.Geometry.Point([[73.8417693187197, 18.436935449462606]]), 30),
    #     'Jambhulwadi' : ([20, 0], ee.Geometry.Point([[73.85916092299954, 18.526407602714407]]), 3)
    # }
    
    collection = imageCollection(date)
    visParams = {'min':0, 'max':1, 
                 'opacity' : 1,
             'palette':['red','blue']
             }
    # layers.addRasterLayers(collection.select(['B2', 'B3', 'B4']).mean(), my_map, 'gotit', visParams)
    collection = layers.ndti(collection, my_map, location)
    print('app')
    print(id(my_map))
    print(dir(my_map.add_to))
    print(my_map.add_to)
    #get center at Khadakwasla
    my_map.add_child(folium.LayerControl())
    print('get')
    return my_map.get_root().render()

