import requests
import boto3
import json
from datetime import datetime, timedelta
import configparser

# --- Configuration ---
config = configparser.ConfigParser()
config.read('config.ini')

S3_BUCKET_NAME = config['AWS']['bucket_name']
LATITUDE = config['Location']['latitude']
LONGITUDE = config['Location']['longitude']
TIMEZONE = config['Location']['timezone']

def run_weather_etl():
    """
    Main function to run the ETL process for daily weather data.
    """
    print("Starting weather ETL process...")

    # --- EXTRACT ---
    # We now fetch data for two days ago to ensure it's in the archive.
    date_to_fetch = (datetime.now() - timedelta(2)).strftime('%Y-%m-%d')
    
    api_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}&start_date={date_to_fetch}&end_date={date_to_fetch}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone={TIMEZONE}"
    )
    
    print(f"Extracting data for date: {date_to_fetch}")
    response = requests.get(api_url)
    response.raise_for_status()
    raw_data = response.json()
    print("Successfully extracted raw data.")

    print("\n--- Raw Data ---")
    print(json.dumps(raw_data, indent=4))

    # --- TRANSFORM ---
    daily_data = raw_data.get('daily', {})
    
    summary = {
        'date': daily_data.get('time', [None])[0],
        'max_temp_celsius': daily_data.get('temperature_2m_max', [None])[0],
        'min_temp_celsius': daily_data.get('temperature_2m_min', [None])[0],
        'total_precipitation_mm': daily_data.get('precipitation_sum', [None])[0]
    }
    
    if summary['max_temp_celsius'] is not None and summary['min_temp_celsius'] is not None:
        summary['avg_temp_celsius'] = round((summary['max_temp_celsius'] + summary['min_temp_celsius']) / 2, 2)
    else:
        summary['avg_temp_celsius'] = None
        
    print(f"Transformed data summary created.")
    
    print("\n--- Processed Data ---")
    print(json.dumps(summary, indent=4))

    # --- LOAD ---
    s3_client = boto3.client('s3')
    
    raw_data_key = f"raw-data/weather_{date_to_fetch}.json"
    processed_data_key = f"processed-data/summary_{date_to_fetch}.json"
    
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=raw_data_key,
        Body=json.dumps(raw_data)
    )
    print(f"Loaded raw data to s3://{S3_BUCKET_NAME}/{raw_data_key}")
    
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=processed_data_key,
        Body=json.dumps(summary)
    )
    print(f"Loaded processed data to s3://{S3_BUCKET_NAME}/{processed_data_key}")
    
    print("Weather ETL process completed successfully.")

if __name__ == "__main__":
    run_weather_etl()