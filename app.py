from flask import Flask
import folium
from authenticate import ee
from imageCollection import imageCollection
from gee import gee
from basemap import basemaps
from cloud_mask import maskS2clouds
# def authenticate():
#     ee.Authenticate()
#     ee.Initialize()
# authenticate()
app = Flask(__name__)

@app.route("/")
def fullscreen():
    """Simple example of a fullscreen map."""
    m = folium.Map()
    # vis_params = {
    #     'min': 0,
    #     'max': 4000,
    #     'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
    #     }

# Create a folium map object.
    my_map = folium.Map(location=[20, 0], zoom_start=3, height=500)
    basemaps['Google Maps'].add_to(my_map)
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    gee(my_map)
    my_map.add_child(folium.LayerControl())
    return my_map.get_root().render()