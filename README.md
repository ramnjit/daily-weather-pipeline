# Daily Weather ETL Pipeline

## 📝 Synopsis

This project is a simple, daily ETL (Extract, Transform, Load) data pipeline written in Python. It's designed to showcase foundational data engineering concepts and hands-on experience with AWS.

The pipeline performs the following steps:
1.  **Extract:** Fetches the previous day's weather data for a configured location from the Open-Meteo API.
2.  **Transform:** Calculates simple summary statistics (e.g., average temperature).
3.  **Load:** Saves both the raw and the processed summary data as JSON files to an AWS S3 bucket.

## 🛠️ Tech Stack

* **Language:** Python
* **Libraries:** Requests (for API calls), Boto3 (AWS SDK)
* **Cloud Platform:** AWS S3

## ⚙️ Setup & Installation

To run this project, you will need an AWS account and Python installed.

1.  **Clone the Repository:**
    ```bash
    git clone [your-repo-url]
    cd daily-weather-pipeline
    ```
2.  **Set up AWS:**
    * Create a private **S3 bucket**.
    * Create an **IAM User** with programmatic access and a permission policy that allows `s3:PutObject` actions on your bucket.
    * Configure your local machine with the user's credentials by running `aws configure`.

3.  **Configure the Project:**
    * Create a copy of the `config.ini.template` file and name it `config.ini`.
    * Edit `config.ini` and enter your S3 bucket name.

4.  **Install Dependencies:**
    * Create and activate a Python virtual environment:
        ```bash
        python -m venv venv
        source venv/bin/activate  # On macOS/Linux
        .\venv\Scripts\activate  # On Windows
        ```
    * Install the required libraries:
        ```bash
        pip install -r requirements.txt
        ```

## ▶️ Usage

Run the pipeline from your terminal:
```bash
python pipeline.py