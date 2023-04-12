# Run application using python app.run
from flask import Flask
import folium
from folium.plugins import Draw, Search
import ee
from basemap import basemaps
# def authenticate():
#     ee.Authenticate()
#     ee.Initialize()
# authenticate()
app = Flask(__name__)

@app.route("/")
def fullscreen():
    class ClickForOneMarker(folium.ClickForMarker):
        _template = Template(u"""
        {% macro script(this, kwargs) %}
        var new_mark = L.marker();
        function newMarker(e){
        new_mark.setLatLng(e.latlng).addTo({{this._parent.get_name()}});
        new_mark.setZIndexOffset(-1);
        new_mark.on('dblclick', function(e){
        {{this._parent.get_name()}}.removeLayer(e.target)})
        var lat = e.latlng.lat.toFixed(4),
        lng = e.latlng.lng.toFixed(4);
        new_mark.bindPopup(
        "<a href=https://www.google.com/maps?layer=c&cbll=" + lat + "," + lng + " target=blank><img src=img/streetview.svg width=70 title=StreetView class=StreetViewImage></img></a>",{
        maxWidth: "auto",
        className: 'StreetViewPopup'
        });
        };
        {{this._parent.get_name()}}.on('click', newMarker); 
        {% endmacro %}
        """) # noqa
        """Simple example of a fullscreen map."""
    def __init__(self, popup=None):
        super(ClickForOneMarker, self).__init__()
        self._name = 'Google Street View'
    gsv = ClickForOneMarker()
    map.add_child(gsv)
    #m = folium.Map()
    vis_params = {
        'min': 0,
        'max': 4000,
        'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}
    
    # points = {
    # "type": "FeatureCollection",
    # "features": [
    #     {
    #         "type": "Feature",
    #         "properties": {
    #             "name": "one"
    #         },
    #         "geometry": {
    #             "type": "Point",
    #             "coordinates": [18.41, 73.74]
    #             }
    #         }
    #     ]
    # }

# Create a folium map object.
# folium.Map(location=[45.5236, -122.6750], zoom_start=13)
    #my_map = folium.Map(location=[18.41, 73.74],tiles = 'cartodbpositron',zoom_start=4)

    # geojson_obj = folium.GeoJson(points, 
    #           marker = folium.Marker(icon=folium.Icon(
    #                                  icon_color='#ff033e',
    #                                  icon='certificate',
    #                                  prefix='fa'))      
    #                     ).add_to(my_map)

    # statesearch = Search(layer=geojson_obj,
    #                  geom_type='Point',
    #                  placeholder="Search",
    #                  collapsed=True,
    #                  search_label='name',
    #                  search_zoom=14,
    #                  position='topright'
    #                 ).add_to(my_map)
    my_map = folium.Map(location=[18.41, 73.74], zoom_start=12, tiles="Stamen Terrain")
    tooltip = "Click me!"

    # Draw(
    # export=True,
    # filename="my_data.geojson",
    # position="topleft",
    # draw_options={"polyline": {"allowIntersection": False}},
    # edit_options={"poly": {"allowIntersection": False}},
    # ).add_to(my_map)
   

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

    

    return my_map.get_root().render()

if __name__ == '__main__':
    app.run()

