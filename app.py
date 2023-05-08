from flask import Flask, request, render_template, jsonify
import folium
from authenticate import ee
from imageCollection import imageCollection
from basemap import basemaps
import layers
from datetime import datetime

import os
import json
import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
from ndti_values import ndti_values

from folium import plugins

app = Flask(__name__)
collection = ee.Image


# def get_coordinates():
#     if os.path.exists('my_data.json'):
#         with open('my_data.json') as f:
#             data = json.load(f)

#         coordinates = []
#         for feature in data['features']:
#             coordinates.append(feature['geometry']['coordinates'])

#         os.remove('my_data.json')
#         return coordinates

#     else:
#         return None


# create the Observer and EventHandler objects
# event_handler = FileSystemEventHandler()
# observer = Observer()
# observer.schedule(event_handler, path='.', recursive=False)

# define the event handler's on_created() method to be called
# when a file is created in the watched directory


# class MyHandler(FileSystemEventHandler):

#     def on_created(self, event):
#         if event.is_directory:
#             return -1
#         elif event.src_path.endswith(".json"):
#             time.sleep(1)
#             coordinates = get_coordinates()
#             if coordinates != None:
#                 # print(coordinates)
#                 # print(coordinates[0])
#                 for i in range(len(coordinates)):
#                     graph_num = i
#                     ndti(graph_num=graph_num, coordinates=coordinates[i])
#                     graph_num += 1

# do something with the coordinates here


# add the event handler to the Observer and start it
# event_handler = MyHandler()
# observer = Observer()
# observer.schedule(event_handler, path='.', recursive=False)
# observer.start()
file_dir = 'templates'
file_name = 'map.html'

# Create the directory if it doesn't exist
if not os.path.exists(file_dir):
    os.makedirs(file_dir)


@app.route("/")
def home():
    my_map = folium.Map(
        location=[18.409749, 73.700581], zoom_start=12, height=1000)
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    my_map.add_child(folium.LayerControl())
    # Save the map object as an HTML file in the specified directory
    my_map.save(os.path.join(file_dir, file_name))
    return render_template('index.html')


@app.route('/map.html')
def test():
    return render_template('map.html')

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

@app.route("/submit_data", methods=['POST'])
def submit_data():

    def convertdate(givendate):

        # convert the date string to a datetime object
        date_obj = datetime.strptime(givendate, '%d-%m-%Y')
        # convert the datetime object to a string in 'YYYY-MM-DD' format
        date_formatted = date_obj.strftime('%Y-%m-%d')
        return date_formatted
    print(dir(request))

    date_from = request.form['datefrom']
    date_to = request.form['dateto']
    location = request.form['location']
    print("details"+date_from, date_to, location)
    # if not date_from or not date_to or not location:
    #     error_message = 'Please fill in all the required fields.'
    #     return render_template('index.html', error_message=error_message)

    # date = ('2023-01-01', '2023-02-15')
    # location = 'Khadakwasla'
    date = (convertdate(date_from), convertdate(date_to))

    # Define a function to handle the draw:created event
    def on_draw_created(e):
        # Get the marker that was created
        marker = e.layer
        # Add a popup to the marker
        marker.bind_popup('Marker added')

    my_map = folium.Map(
        location=[18.409749, 73.700581], zoom_start=12, height=1000)
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    global collection
    # collection = imageCollection(date)
    
    collection = layers.ndti(date, my_map, location)
    my_map.add_child(folium.LayerControl())
    # my_map.add_child(folium.LayerControl())
    tooltip = "Click me!"

    draw_data = plugins.Draw(export=False, position='topleft', draw_options={'marker': True, 'polyline': False,
                                                                             'polygon': False,
                                                                             'rectangle': False,
                                                                             'circle': False,
                                                                             'circlemarker': False}, edit_options={'edit': False})

    draw_data.add_to(my_map)

    

    repl = "alert(coords);"

    # s = my_map._repr_html_()
    my_map.save(os.path.join(file_dir, file_name))

    # Open and read the HTML file contents into a variable
    with open(os.path.join(file_dir, file_name), 'r') as file:
        html_string = file.read()

    # Print the HTML string
    # print(html_string)

    rep = """
                window.parent.showGraphs(coords);        
        """

    replaced = html_string.replace(repl, rep)
    with open(os.path.join(file_dir, file_name), 'w') as file:
        file.write(replaced)

    # replaced.save(os.path.join(file_dir, file_name))

    return render_template('index.html')

# global graph_num = 0


@app.route('/getCoordinates', methods=['POST'])
def get_Coordinates():
    if request.method == 'POST':
        Coordinates = request.get_json()
    # get the JSON data from the request body

        Coordinates = json.loads(Coordinates)
        # print(type(Coordinates))
        # print(Coordinates['geometry']['coordinates'])

        respo = ndti_values(
            None, Coordinates['geometry']['coordinates'], collection)
        #print(respo, type(respo))
        ls = list(respo.values())
        print(ls, type(ls), len(ls), ls[0])
        if ls[0] == None:
            return jsonify({'success': False }), 200
            
        ls_dates = list(respo.keys())
        Dates = []
        NDTI_values = []
        sum = 0.0
        for i, j in zip(ls, ls_dates):
            # Convert the date string to a datetime object
            date_obj = datetime.strptime(j, '%Y%m%d')

            # Format the datetime object as a string in DD/MM/YYYY format
            formatted_date_str = date_obj.strftime('%d/%B/%Y')
            Dates = Dates + [formatted_date_str]
            NDTI_values = NDTI_values + [i]
            sum = sum + i
        mean = sum / float(len(ls))

        print(Dates)
        print(NDTI_values)
        print(respo)

        # graph_num += 1
        # return a success response
        return jsonify({'success': True, 'Dates': Dates, 'ndtivalues': NDTI_values, 'meanvalue': mean, 'Coordinates': Coordinates['geometry']['coordinates']}), 200
    else:
        # return an error response if the request method is not POST
        return jsonify({'error': 'Invalid request method'}), 405


@app.route('/ExportAllCord', methods=['POST'])
def Export_All_Cord():
    if request.method == 'POST':
        AllCord = request.get_json()
    # get the JSON data from the request body
        print("******************************", AllCord)
        # AllCord = json.loads(AllCord)
        print(type(AllCord))


        # graph_num += 1
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


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
