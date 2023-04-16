from flask import Flask, request, render_template, jsonify
import folium
from authenticate import ee
from imageCollection import imageCollection
from basemap import basemaps
import layers
from datetime import datetime

# def authenticate():
#     ee.Authenticate()
#     ee.Initialize()
# authenticate()
app = Flask(__name__)
collection = ee.ImageCollection


@app.route("/")
def home():
    my_map = folium.Map(
        location=[18.409749, 73.700581], zoom_start=12, height=1000)
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    # my_map.add_child(folium.LayerControl())
    return render_template('index.html', my_map=my_map._repr_html_())

# def fullscreen():
#     my_map = folium.Map(location=[18.409749, 73.700581], zoom_start=3, height=1000)
#     basemaps['Google Satellite Hybrid'].add_to(my_map)
#     # my_map.add_child(folium.LayerControl())
#     if request.method == 'GET':
#         print('post')
#         return render_template('index.html', my_map=my_map._repr_html_())
#         # return my_map.get_root().render()
#     data = request.get_json()  # get the JSON data from the request body
#         # do something with the data, e.g. store it in a database
#     print(data)  # print the data to the console
#     date = ('2023-01-01', '2023-02-15')
#     location = 'Khadakwasla'
#     # locations = {
#     #     'Khadakwasla' : ([20, 0], ee.Geometry.Point([[73.73801385248593, 18.412317318279012]]), 3),
#     #     'Mula mutha' : ([20, 0], ee.Geometry.Point([[73.8417693187197, 18.436935449462606]]), 30),
#     #     'Jambhulwadi' : ([20, 0], ee.Geometry.Point([[73.85916092299954, 18.526407602714407]]), 3)
#     # }

#     collection = imageCollection(date)
#     visParams = {'min':0, 'max':1,
#                  'opacity' : 1,
#              'palette':['red','blue']
#              }
#     # layers.addRasterLayers(collection.select(['B2', 'B3', 'B4']).mean(), my_map, 'gotit', visParams)
#     collection = layers.ndti(collection, my_map, location)
#     print('app')
#     print(id(my_map))
#     print(dir(my_map.add_to))
#     print(my_map.add_to)
#     #get center at Khadakwasla
#     my_map.add_child(folium.LayerControl())
#     print('get')
#     # return my_map.get_root().render()
#     return render_template('index.html', my_map=my_map._repr_html_())



# @app.route('/submitdata', methods=['POST'])
# def submit_data():
   

#         data = request.get_json()  # get the JSON data from the request body

       
#         dates = (data['P_fromdate'], data['P_todate'])
#         print(dates)  # print the data to the console
#         location = data['P_selocation']

#         locations = {
#             'Khadakwasla' : [18.412317318279012, 73.73801385248593 ],
#             'Mula mutha' : [73.8417693187197, 18.436935449462606],
#             'Jambhulwadi' :[73.85916092299954, 18.526407602714407]
#         }
#         print('*******************************')
#         print(locations[location])
#         my_map = folium.Map(location=[18.409749, 73.700581], zoom_start=5, height=1000)
#         basemaps['Google Satellite Hybrid'].add_to(my_map)

#         collection = imageCollection(dates)
#         collection = layers.ndti(collection, my_map, location)

#         my_map.add_child(folium.LayerControl())
#         print('******************DONE***********************')
        
#         return render_template('index.html', my_map=my_map._repr_html_())

        # return jsonify({'success': True}), 200  # return a success response
   
@app.route("/submitdata", methods=['POST'])
def submit_data():
    # date_from = request.form['datefrom']
    # date_to = request.form['dateto']

    # def convertdate(givendate):

    # # convert the date string to a datetime object
    #     date_obj = datetime.strptime(givendate, '%d-%m-%Y')

    # # convert the datetime object to a string in 'YYYY-MM-DD' format
    #     date_formatted = date_obj.strftime('%Y-%m-%d')
    #     return date_formatted
    # # data = request.get_json()  # get the JSON data from the request body
    # print(convertdate(date_from))
    date = ('2023-01-01', '2023-02-15')
    location = 'Khadakwasla'
    my_map = folium.Map(
        location=[18.409749, 73.700581], zoom_start=12, height=1000)
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    collection = imageCollection(date)
    collection = layers.ndti(collection, my_map, location)
    my_map.add_child(folium.LayerControl())
    print("sdvsvkjb")
    return render_template('index.html', my_map=my_map._repr_html_())
    # return render_template('hello.html')

@app.route('/getCoordinates', methods=['POST'])
def get_Coordinates():
    if request.method == 'POST':
        Coordinates = request.get_json()  # get the JSON data from the request body
        # do something with the data, e.g. store it in a database
        print(Coordinates)  # print the data to the console
        return jsonify({'success': True}), 200  # return a success response
    else:
        # return an error response if the request method is not POST
        return jsonify({'error': 'Invalid request method'}), 405

# @app.route('/')
# def index():
#     # create a Folium map object
#     my_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)
#     map_style = {
#         'position': 'absolute',
#         'width': '100.0%',
#         'height': '500px',  # set the height to a fixed pixel value
#         'left': '0.0%',
#         'top': '0.0%',
#         'z-index': 0
#     }

#     # render the HTML template and pass the map object and CSS styles as variables
#     return render_template('hello.html', my_map=my_map._repr_html_(), map_style=map_style)
