#import threading
from authenticate import ee
from gee import imageCollection
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
#import seaborn as sns

graph_num = 0
def ndti(coordinates):
    global graph_num
    
    #l = []
    # for i in cordinates:
    #     l.append(ee.Geometry.Point(i))
    #print(coordinates)
    #geometry = ee.Geometry.Point([73.50502848893966,18.09751560212352])
    geometry = ee.Geometry.Point(coordinates)

    # imageCollection = imageCollection.select(['B2', 'B3', 'B4'])
    imageCollection = ee.ImageCollection('COPERNICUS/S2_SR').filterDate(
        '2023-02-01', '2023-04-12').select(['B2', 'B3', 'B4']).filterBounds(geometry=geometry)
    # def conditional(image, list):
    #   return ee.List(list).add(image.reduceRegion(ee.Reducer.toList(), geometry, 10))

    # ls = imageCollection.iterate(conditional, ee.List([]))
    # print(ls.getInfo())
    tobands_image = imageCollection.toBands()
    # def get_ndti(image):
    reduced = tobands_image.reduceRegion(
        reducer=ee.Reducer.first(),
        geometry=geometry,
        bestEffort=True,
        scale=10).getInfo()
    dic = {j[:8]: [] for j in list(reduced.keys())[::3]}
    #count = 0
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

    #print("DIC= ", dic)

    # Extract the date and turbidity data from the dictionary
    dates = list(dic.keys())
    turbidity_values = list(dic.values())

    #
    # Create a line chart of the turbidity data
    plt.plot(dates, turbidity_values)
    plt.title('Turbidity over time')
    plt.xlabel('Date')
    plt.ylabel('Turbidity')
    plt.xticks(rotation=45)
    # Save the graph as a PNG image file
    plt.savefig(f'graphs/{coordinates}.png')
    # plt.clf()
    # plt.show()

    # Create a bar chart of the turbidity data

    # plt.bar(dates, turbidity_values)
    # plt.title('Turbidity over time')
    # plt.xlabel('Date')
    # plt.ylabel('Turbidity')
    # plt.xticks(rotation=45)
    # # Save the graph as a PNG image file
    # plt.savefig(f'graphs/bar_chart_{graph_num}.png')
    # plt.show()
    plt.clf()
    graph_num += 1
    # Start a new thread to run the plot_data function
    # thread = threading.Thread(target=plot_data)
    # thread.start()

    # # Wait for the thread to finish before exiting the program
    # thread.join()


# Combined Charts

# fig, ax1 = plt.subplots()

# # Create the line chart
# color = 'tab:blue'
# ax1.set_xlabel('Date')
# ax1.set_ylabel('Turbidity', color=color)
# ax1.plot(dates, turbidity_values, color=color)
# ax1.tick_params(axis='y', labelcolor=color)

# # Create the bar chart
# ax2 = ax1.twinx() # Share the x-axis
# color = 'tab:red'
# ax2.set_ylabel('Turbidity', color=color)
# ax2.bar(dates, turbidity_values, color=color, alpha=0.3)
# ax2.tick_params(axis='y', labelcolor=color)

# # Set the x-axis labels and rotation
# ax1.set_xticks(range(len(dategraph_nums)))
# ax1.set_xticklabels(dates, rotation=45, ha='right')

# # Set the chart title
# plt.title('Turbidity over time')

# # Save the graph as a PNG image file
# plt.savefig('graphs/combined_chart.png')

# # Show the chart
# #plt.show()