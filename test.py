from flask import Flask, request, render_template, jsonify, json
import folium
from authenticate import ee
from imageCollection import imageCollection
from basemap import basemaps
import layers
from datetime import datetime
from folium import plugins

# def authenticate():
#     ee.Authenticate()
#     ee.Initialize()
# authenticate()
app = Flask(__name__)
collection = ee.ImageCollection


def submit_data():
 
    # if not date_from or not date_to or not location:
    #     error_message = 'Please fill in all the required fields.'
    #     return render_template('index.html', error_message=error_message)

    date = ('2023-01-01', '2023-02-15')
    location = 'Khadakwasla'
    my_map = folium.Map(
        location=[18.409749, 73.700581], zoom_start=12, height=1000)
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    draw_data = plugins.Draw(export=False,position='topleft', draw_options={'marker': True, 'polyline': False, 
                                                                 'polygon': False,
                                                                 'rectangle': False,
                                                                 'circle': False,
                                                                 'circlemarker': False}, edit_options={'edit': False})  
    
    draw_data.add_to(my_map)
    
    collection = imageCollection(date)
    collection = layers.ndti(collection, my_map, location)
    my_map.add_child(folium.LayerControl())
    # print("sdvsvkjb")
    # map_id = my_map.get_name()
    # print("Map ID:", map_id)
    my_map.save('test.html')
    # return render_template('index.html', my_map=my_map._repr_html_())

submit_data()

