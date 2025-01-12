from flask import Flask, request, jsonify, send_from_directory
from scipy.spatial import cKDTree
import numpy as np
import pandas as pd
from geopy.distance import geodesic


#init our search tree
coordinates_loaded = np.load("data/coordinates.npy")
df_loaded = pd.read_csv("data/waves_data.csv")
tree = cKDTree(coordinates_loaded)

def find_nearest_in_df(lat, lon):
    query_point = np.array([lon, lat])
    distance, index = tree.query(query_point)
    nearest_row = df_loaded.iloc[index]
    return nearest_row


app = Flask(__name__)

#app is served at localhost:5000
@app.route('/')
def index():
  return send_from_directory('static', 'interactive_map.html')


#51.5072° N, 0.1276° W london
#52.5200° N, 13.4050° E Berlin
#-41.2732° S, 173.2854° E lat lon of nelson nz
#These coords match our map, therefore problem with points on land probably comes from 
#1)error in dataset
#2) different coordinate/projection system used in dataset

@app.route('/query_coords', methods=['GET'])
def get_wave_height():
  lat = float(request.args.get('lat'))
  lon = float(request.args.get('lon'))
  
  #query our search tree to find closest data point
  try:
    df_row = find_nearest_in_df(lat, lon)
    nearest_lat, nearest_lon, max_wave_height = df_row['latitude'], df_row['longitude'], round(df_row['hmax'], 3)
    distance = round(geodesic((lat, lon), (nearest_lat, nearest_lon)).km, 3)
  except Exception as E:
    print('Error processing search: ', E)
    return '', 500

  return jsonify({
    "distance": distance,
    "wave_height": max_wave_height,
    "lat" : nearest_lat,
    "lon" : nearest_lon,
  })


if __name__ == "__main__":
    app.run(debug=True)


