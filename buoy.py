from flask import Flask, request, jsonify, send_from_directory
import xarray as xr
import math
from geopy.distance import geodesic

ds = xr.open_dataset("data/waves_2019-01-01.nc")
app = Flask(__name__)

#app is served at localhost:5000
@app.route('/')
def index():
  return send_from_directory('.', 'interactive_map.html')


@app.route('/query_coords', methods=['GET'])
def get_wave_height():
  lat = float(request.args.get('lat'))
  lon = float(request.args.get('lon'))

  max_wave_data = ds.sel(latitude=lat, longitude=lon, method="nearest")['hmax'].max()
  max_wave_height = round(max_wave_data.item(), 3)

  #currently there exist some datapoints without any wave height data. TODO: remove these from dataset
  #for now, we just return a helpful message if the user has selected such a datapoint
  if math.isnan(max_wave_height):
    return jsonify({"success": False, "message": "No observations near this point", "lat" : lat, "lon" : lon })
  else:
    observation_coords = max_wave_data.coords["latitude"].item(), max_wave_data.coords["longitude"].item()
    distance = round(geodesic((lat, lon), observation_coords).km, 3)
    return jsonify({"success": True, "distance": distance, "wave_height": max_wave_height, "lat" : observation_coords[0], "lon" : observation_coords[1] })

if __name__ == "__main__":
    app.run(debug=True)


