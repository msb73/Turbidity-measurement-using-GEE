from flask import Flask, render_template
import folium
from folium import plugins
from folium import plugins
import ee
from basemap import basemaps

def fullscreen():
    #m = folium.Map()
    vis_params = {
        'min': 0,
        'max': 4000,
        'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}
    
    my_map = folium.Map(location=[18.41, 73.74], zoom_start=12, tiles="Stamen Terrain")
    #tooltip = "Click me!"

    # folium.Marker(
    # [18.41, 73.74], popup="<i>Khadakwasla</i>", tooltip=tooltip
    # ).add_to(my_map)

    # folium.Marker(
    # [18.4323, 73.7624], popup="<i>Khadakwasla</i>", tooltip=tooltip
    # ).add_to(my_map)

    # folium.Marker(
    # [18.3946, 73.7022], popup="<i>Khadakwasla</i>", tooltip=tooltip
    # ).add_to(my_map)

    draw_data = plugins.Draw(export=False,position='topleft', draw_options={'marker': True, 'polyline': False, 
                                                                 'polygon': False,
                                                                 'rectangle': False,
                                                                 'circle': False,
                                                                 'circlemarker': False}, edit_options={'edit': False})  
    
    draw_data.add_to(my_map)
    
    
    # folium.Marker(
    # [18.3964, 73.6724], popup="<i>Khadakwasla</i>", tooltip=tooltip
    # ).add_to(my_map)
    ### GRAPHS CODE START
    import json
    import requests

    url = (
        "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
    )
    vis3 = json.loads(requests.get(f"{url}/vis2.json").text)
    folium.Marker(
    location=[18.3964, 73.672],
    popup=folium.Popup(max_width=450).add_child(
        folium.Vega(vis3, width=450, height=250)
    ),
    ).add_to(my_map)
    ### GRAPH CODE END

    basemaps['Google Maps'].add_to(my_map)
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    my_map.add_child(folium.LayerControl())

    

    my_map.save('test.html')

fullscreen()