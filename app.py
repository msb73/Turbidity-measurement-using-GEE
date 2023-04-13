# Run application using python app.run
from flask import Flask, render_template,  request, jsonify
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
def home():
    return render_template("index.html")


@app.route('/submitdata', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        data = request.get_json()  # get the JSON data from the request body
        # do something with the data, e.g. store it in a database
        print(data)  # print the data to the console
        return jsonify({'success': True}), 200  # return a success response
    else:
        return jsonify({'error': 'Invalid request method'}), 405  # return an error response if the request method is not POST

if __name__ == '__main__':
    app.run()

