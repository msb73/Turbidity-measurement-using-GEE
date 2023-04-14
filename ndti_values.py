from authenticate import ee
from gee import imageCollection
geometry = ee.Geometry.Point([73.50502848893966,18.09751560212352])

# imageCollection = imageCollection.select(['B2', 'B3', 'B4'])
imageCollection = ee.ImageCollection('COPERNICUS/S2_SR').filterDate('2023-02-01', '2023-04-12').select(['B2', 'B3', 'B4']).filterBounds(geometry=geometry)
# def conditional(image, list):
#     return ee.List(list).add(image.reduceRegion(ee.Reducer.toList(), geometry, 10))

# ls = imageCollection.iterate(conditional, ee.List([]))
# print(ls.getInfo())
tobands_image = imageCollection.toBands()
# def get_ndti(image):
reduced = tobands_image.reduceRegion(
    reducer =  ee.Reducer.first(), 
    geometry =  geometry,
    bestEffort = True,
    scale =  10).getInfo()
dic = {j[:8] : [] for j in list(reduced.keys())[::3]}
count = 0
for i in reduced:
    dic[i[:8]].append(reduced[i])
# print(reduced.getInfo())
# print(dic)
# print(len(dic))
import math

# Define the constants for the ATM model
K = 0.16
alpha = 1.3

# Define a function to convert RGB values to turbidity values using the ATM model
def rgb_to_turbidity(rgb):
    # Convert the RGB values to reflectance
    reflectance = rgb / 10000.0
    
    # Compute the aerosol optical depth (AOD) using the blue band (B2)
    aod = -math.log(reflectance)
    
    # Compute the turbidity coefficient using the ATM model
    turbidity = K * math.pow(aod, alpha)
    
    return turbidity

# Loop through the dictionary and convert the RGB values to turbidity values
# for date in dic:
#     rgb_values = dic[date]
#     turbidity_values = [rgb_to_turbidity(rgb) for rgb in rgb_values]
#     dic[date] = turbidity_values

# Loop through the dictionary and convert the RGB values to mean turbidity values
for date in dic:
    rgb_values = dic[date]
    turbidity_values = [rgb_to_turbidity(rgb) for rgb in rgb_values]
    mean_turbidity = sum(turbidity_values) / len(turbidity_values)
    dic[date] = mean_turbidity


print("DIC= ",dic)

import matplotlib.pyplot as plt

# Extract the date and turbidity data from the dictionary
dates = list(dic.keys())
turbidity_values = list(dic.values())

# Create a line graph of the turbidity data
plt.plot(dates, turbidity_values)

# Set the title and axis labels
plt.title('Turbidity over time')
plt.xlabel('Date')
plt.ylabel('Turbidity')

# Rotate the X-axis labels for better readability
plt.xticks(rotation=45)
plt.savefig('graphs/line_chart.png')
# Display the graph
# plt.show()


# BAR Graph
plt.bar(dates, turbidity_values)

# Set the title and axis labels
plt.title('Turbidity over time')
plt.xlabel('Date')
plt.ylabel('Turbidity')

# Rotate the X-axis labels for better readability
plt.xticks(rotation=45)
plt.savefig('graphs/bar_chart.png')
# Display the graph
# plt.show()