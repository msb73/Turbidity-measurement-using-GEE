#import threading
from authenticate import ee
from gee import imageCollection
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
#import seaborn as sns


def ndti_values(graph_num, cordinates, image):
    geometry = ee.Geometry.MultiPoint(cordinates)
    # print(coordinates)
    #geometry = ee.Geometry.Point([73.50502848893966,18.09751560212352])
    # geometry = ee.Geometry.Point(coordinates)

    # imageCollection = imageCollection.select(['B2', 'B3', 'B4'])
    #######################
    # imageCollection = ee.ImageCollection('COPERNICUS/S2_SR').filterDate(
    #     '2023-02-01', '2023-04-12').select(['B2', 'B3', 'B4']).filterBounds(geometry=geometry)
    # def conditional(image, list):
    #   return ee.List(list).add(image.reduceRegion(ee.Reducer.toList(), geometry, 10))

    # ls = imageCollection.iterate(conditional, ee.List([]))
    # print(ls.getInfo())
    # def get_ndti(image):
    reduced = image.reduceRegion(
        reducer=ee.Reducer.toList(),
        geometry=geometry,
        bestEffort=True,
        scale=10).getInfo()
    dic = {i[:8]: j[0]*10 for i, j in reduced.items()}
    print(dic)

    '''
    
    
    #return dic
    count =0
    # for i in reduced:
    #     dic[i[:8]].append(reduced[i])
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



    # Loop through the dictionary and convert the RGB values to mean turbidity values
    print(dic)
    for date in dic:
        rgb_values = dic[date]
        turbidity_values = [rgb_to_turbidity(rgb) for rgb in rgb_values]
        mean_turbidity = sum(turbidity_values) / len(turbidity_values)
        dic[date] = mean_turbidity
    '''
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
    plt.savefig(f'static/graphs/line_chart.png')
    plt.clf()

    # plt.clf()
    # plt.show()

    # Create a bar chart of the turbidity data

    plt.bar(dates, turbidity_values)
    plt.title('Turbidity over time')
    plt.xlabel('Date')
    plt.ylabel('Turbidity')
    plt.xticks(rotation=45)
    # Save the graph as a PNG image file
    plt.savefig(f'static/graphs/bar_chart.png')
    # plt.show()
    plt.clf()


    import pandas as pd

    # Assuming that `dates` and `turbidity_values` are already defined

    # Create a dictionary with the two lists
    import pandas as pd

    # Define the filename for the Excel file
    filename = 'static/graphs/data.xlsx'

    # Get the dates and turbidity values for this iteration
    dates = list(dic.keys())
    turbidity_values = list(dic.values())

    # Create a new DataFrame for the new data
    new_data = pd.DataFrame({'Date': dates, 'Turbidity': turbidity_values})

    # Read the existing Excel file into a DataFrame, or create a new DataFrame if the file doesn't exist
    try:
        existing_data = pd.read_excel(filename)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    # Append the new data to the existing DataFrame
    updated_data = pd.concat([existing_data, new_data], ignore_index=True)

    # Write the updated DataFrame back to the Excel file
    updated_data.to_excel(filename, index=False)

    return dic
    # Start a new thread to run the plot_data function
    # thread = threading.Thread(target=plot_data)
    # thread.start()

    # # Wait for the thread to finish before exiting the program
    # thread.join()

