from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from pipeline import run_weather_etl 
import sys

# Initialize the Flask web application
application = Flask(__name__)

# Enable CORS to allow the frontend on a different domain to call this API
CORS(application) 

# A simple dictionary to map city names to their coordinates
CITIES = {
    "chicago": {"lat": 41.87, "lon": -87.62, "tz": "America/Chicago"},
    "new_york": {"lat": 40.71, "lon": -74.00, "tz": "America/New_York"},
    "london": {"lat": 51.50, "lon": -0.12, "tz": "Europe/London"},
}

# Simple health check endpoint to confirm the API is running
@application.route("/", methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Main API endpoint that the frontend calls to trigger the ETL process.
@application.route("/run-pipeline", methods=['GET'])
def trigger_pipeline():
    print("API endpoint triggered...", file=sys.stderr)
    try:
        # If no city is provided, it will default to 'chicago'.
        city_key = request.args.get('city', 'chicago')
        city_data = CITIES.get(city_key)

        if not city_data:
            return jsonify({"error": f"City key '{city_key}' not found."}), 400

        # call main ETL function with city's coordinates
        summary_data = run_weather_etl(city_data["lat"], city_data["lon"], city_data["tz"])
        
        # returns processed summary data to the frontend as JSON response
        print(f"DATA SENT: {summary_data}", file=sys.stderr)
        return jsonify(summary_data), 200
        
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return jsonify({"error": str(e)}), 500