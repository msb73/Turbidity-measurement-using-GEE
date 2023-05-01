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
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ndti_values import ndti_values

print('###############################################################################################')
app = Flask(__name__)
image = ee.Image


def get_coordinates():
    if os.path.exists('my_data.json'):
        with open('my_data.json') as f:
            data = json.load(f)

        coordinates = []
        for feature in data['features']:
            coordinates.append(feature['geometry']['coordinates'])

        os.remove('my_data.json')
        return coordinates

    else:
        return None


# create the Observer and EventHandler objects
event_handler = FileSystemEventHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)

# define the event handler's on_created() method to be called
# when a file is created in the watched directory


class MyHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return -1
        elif event.src_path.endswith(".json"):
            time.sleep(1)
            coordinates = get_coordinates()
            if coordinates != None:
                # print(coordinates)
                # print(coordinates[0])
                for i in range(len(coordinates)):
                    graph_num = i
                    ndti(graph_num=graph_num, coordinates=coordinates[i])
                    graph_num += 1

            # do something with the coordinates here


# add the event handler to the Observer and start it
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)
observer.start()


@app.route("/")
def home():
    my_map = folium.Map(
        location=[18.409749, 73.700581], zoom_start=12, height=1000)
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    # my_map.add_child(folium.LayerControl())
    return render_template('index.html', my_map=my_map._repr_html_())

@app.route("/submit_data", methods=['POST'])
def submit_data():            # after submit button return map with layer
    def convertdate(givendate):

        # convert the date string to a datetime object
        date_obj = datetime.strptime(givendate, '%d-%m-%Y')
        # convert the datetime object to a string in 'YYYY-MM-DD' format
        date_formatted = date_obj.strftime('%Y-%m-%d')
        return date_formatted
    data = request.get_json()
    date_from = data['P_fromdate']
    date_to = data['P_todate']
    location = data['P_selocation']
    print('location')
    print(data)
    if not date_from or not date_to or not location:
        error_message = 'Please fill in all the required fields.'
        return render_template('index.html', error_message=error_message)

    # date = ('2023-01-01', '2023-02-15')
    date = (convertdate(date_from), convertdate(date_to))

    my_map = folium.Map(
        location=[18.409749, 73.700581], zoom_start=12, height=1000)
    basemaps['Google Satellite Hybrid'].add_to(my_map)
    global image
    # inner_coll = imageCollection(date)
    image = layers.ndti(date,  my_map, location)
    my_map.add_child(folium.LayerControl())
    print("sdvsvkjb")
    #########################################
    ################ MINE ###################
    #########################################
    points = ee.Geometry.MultiPoint(
    [[73.74118158587497, 18.4148644079408],
     [73.7428981996445, 18.41983191088514],
     [73.74650308856052, 18.423740664826617],
     [73.73268434771579, 18.408349432637745],
     [73.73963663348239, 18.410466826659608],
     [73.73440096148532, 18.411932699571228],
     [73.73663255938571, 18.40859374866174],
     [73.86408499021032, 18.47600873142659]])
    dic = ndti_values(None, points, image)
    print(dic)
    return render_template('index.html', my_map=my_map._repr_html_())


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


