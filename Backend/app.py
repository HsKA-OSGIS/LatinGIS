from flask import Flask, request, jsonify
from shapely.geometry import Point
import geopandas as gpd
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Function to fetch data from an external API
def fetch_external_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

# Function to load point data from GeoJSON files
def load_point_data_from_geojson(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"GeoJSON file not found: {filename}")
        return None

# Use environment variables for external API URLs
external_api_url_1 = os.getenv('EXTERNAL_API_URL_1', 'https://example.com/points1')
external_api_url_2 = os.getenv('EXTERNAL_API_URL_2', 'https://example.com/points2')
external_api_url_3 = os.getenv('EXTERNAL_API_URL_3', 'https://example.com/points3')

# Sample point data (replace with your actual data or load from GeoJSON files)
point_data_1 = load_point_data_from_geojson(os.path.join('data', 'point_data1.geojson'))
point_data_2 = load_point_data_from_geojson(os.path.join('data', 'point_data2.geojson'))
point_data_3 = load_point_data_from_geojson(os.path.join('data', 'point_data3.geojson'))

# Endpoint for calculating buffer zones
@app.route('/calculate_buffers', methods=['POST'])
def calculate_buffers():
    data = request.get_json()

    # Attempt to fetch data from the external API for each layer
    external_data_1 = fetch_external_data(external_api_url_1)
    external_data_2 = fetch_external_data(external_api_url_2)
    external_data_3 = fetch_external_data(external_api_url_3)

    # Choose which layer to use based on availability
    if external_data_1:
        point_data = external_data_1
    elif external_data_2:
        point_data = external_data_2
    elif external_data_3:
        point_data = external_data_3
    else:
        # Fall back to loading point data from GeoJSON file for the first layer
        point_data = load_point_data_from_geojson(os.path.join('data', 'point_data1.geojson'))

    user_location = Point(data['latitude'], data['longitude'])

    buffer_zones = {}

    for point_name, point_coords in point_data.items():
        point = Point(point_coords['latitude'], point_coords['longitude'])

        # Calculate buffer zone (using 1 km radius for simplicity)
        buffer_zone = point.buffer(1)

        buffer_zones[point_name] = buffer_zone

    # Convert buffer zones to GeoJSON and send as response
    response_data = {
        'buffer_zones': gpd.GeoSeries(buffer_zones).to_json()
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
