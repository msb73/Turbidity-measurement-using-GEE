from flask import Flask, render_template
import folium
from folium.plugins import Draw, Search
import ee
from basemap import basemaps

def fullscreen():
    #m = folium.Map()
    vis_params = {
        'min': 0,
        'max': 4000,
        'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}
    
    my_map = folium.Map(location=[18.41, 73.74], zoom_start=12, tiles="Stamen Terrain")
    tooltip = "Click me!"

    folium.Marker(
    [18.41, 73.74], popup="<i>Khadakwasla</i>", tooltip=tooltip
    ).add_to(my_map)

    folium.Marker(
    [18.4323, 73.7624], popup="<i>Khadakwasla</i>", tooltip=tooltip
    ).add_to(my_map)

    folium.Marker(
    [18.3946, 73.7022], popup="<i>Khadakwasla</i>", tooltip=tooltip
    ).add_to(my_map)

    folium.Marker(
    [18.3964, 73.6724], popup="<i>Khadakwasla</i>", tooltip=tooltip
    ).add_to(my_map)
    # folium.Marker(location =[data.iloc[i]['lat'], data.iloc[i]['lon']], 
    #               popup =data.iloc[i]['name'], icon = folium.Icon(color ='red')).add_to(n)

    basemaps['Google Maps'].add_to(my_map)
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    my_map.add_child(folium.LayerControl())

    

    my_map.save('fol.html')

fullscreen()