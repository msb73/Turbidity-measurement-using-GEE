import json
import os
def get_coordinates():
    with open('my_data.json') as f:
        data = json.load(f)

    coordinates = []
    for feature in data['features']:
        coordinates.append(feature['geometry']['coordinates'])

    os.remove('my_data.json')
    return coordinates
