import requests
import boto3
import json
from datetime import datetime, timedelta
import configparser
import os
import sys

def run_weather_etl(latitude, longitude, timezone):
    """
    Extracts, Transforms, and Loads weather data for a given location.
    """
    print("ETL function started...", file=sys.stderr)

    # Configuration
    # Load the S3 bucket name from the config.ini file to keep it separate from the code.
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    config.read(config_path)
    S3_BUCKET_NAME = config['AWS']['bucket_name']
    print("Config loaded.", file=sys.stderr)

    # EXTRACT
    # Gets yesterdays date as target for data poll
    date_to_fetch = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    
    # Constructs URL for the Open-Meteo API with the specified coordinates and date
    api_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&start_date={date_to_fetch}&end_date={date_to_fetch}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone={timezone}"
    )
    
    # Makes the HTTP GET request to the external API
    print(f"Extracting data for date: {date_to_fetch}", file=sys.stderr)
    response = requests.get(api_url)
    response.raise_for_status()
    raw_data = response.json()

    # TRANSFORM
    # Parses JSON response and pulls out only the key values we need
    daily_data = raw_data.get('daily', {})
    summary = {
        'date': daily_data.get('time', [None])[0],
        'max_temp_celsius': daily_data.get('temperature_2m_max', [None])[0],
        'min_temp_celsius': daily_data.get('temperature_2m_min', [None])[0],
        'total_precipitation_mm': daily_data.get('precipitation_sum', [None])[0]
    }
    
     # Performs simple calculation to create a new data point (average temperature).
    if summary['max_temp_celsius'] is not None and summary['min_temp_celsius'] is not None:
        summary['avg_temp_celsius'] = round((summary['max_temp_celsius'] + summary['min_temp_celsius']) / 2, 2)
    else:
        summary['avg_temp_celsius'] = None
    print("Transform complete.", file=sys.stderr)

    # LOAD
    # Initialize AWS S3 client using the Boto3 library
    s3_client = boto3.client('s3')
    
    # Defines file paths for where to store the data in S3
    raw_data_key = f"raw-data/weather_{date_to_fetch}.json"
    processed_data_key = f"processed-data/summary_{date_to_fetch}.json"
    
    # Upload both the original raw data and our processed summary data to the S3 bucket
    s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=raw_data_key, Body=json.dumps(raw_data))
    s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=processed_data_key, Body=json.dumps(summary))
    print("Load to S3 complete.", file=sys.stderr)
    
    # return summary data to calling function (Flask API)
    return summary