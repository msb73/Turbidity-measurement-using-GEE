# Run application using python app.run
from flask import Flask, render_template
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
    return render_template("fol.html")

if __name__ == '__main__':
    app.run()

