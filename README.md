# 🐍 Interactive Python ETL Web App (Flask & AWS)

This is a full-stack web application that demonstrates a complete data pipeline. The project uses a **Python/Flask** backend (hosted on **AWS Elastic Beanstalk**) to run an ETL script that fetches live data from a public weather API, transforms it, and loads it to an **AWS S3** bucket.

The frontend is a simple, interactive HTML/CSS/JavaScript page (served by Flask) that allows a user to trigger the pipeline and see the processed JSON data in real-time.

## 🚀 Live Interactive Demo

This repository contains the **backend API** for the ETL pipeline.

A live, interactive **frontend demo** of this project (which calls this API) is hosted on my main portfolio website. You can go there right now to select a city and run the pipeline in your browser:

**[https://romanboparai.com/python-etl](https://romanboparai.com/python-etl)**

## Features 🌟

* **Interactive Frontend:** A clean UI built with HTML/CSS that allows a user to select a city.
* **Dynamic Data Fetching:** JavaScript `fetch()` calls the live backend API to run the pipeline on demand.
* **Dynamic Results:** The JSON data returned from the API is dynamically rendered onto the page, including a C°/F° toggle.
* **ETL Backend:** The core logic runs a full Extract, Transform, and Load process.
* **Cloud Deployment:** The entire Flask application is deployed and running on AWS Elastic Beanstalk.

## 🛠️ Tech Stack

* **Backend:** **Python**, **Flask**, **Gunicorn**, **Boto3** (for AWS), **Requests**
* **Frontend:** **HTML5**, **CSS3**, **JavaScript (ES6+)**
* **Cloud:** **AWS Elastic Beanstalk** (for hosting the app), **AWS S3** (for data storage)

## ⚙️ How to Run Locally

To run this project, you will need an AWS account and Python installed.

1.  **Clone the Repository** and `cd` into the folder.

2.  **Set up AWS:**
    * Create a private **S3 bucket**.
    * Create an **IAM User** with programmatic access and a policy that allows `s3:PutObject` on your bucket.
    * Run `aws configure` in your terminal to set up your local credentials.

3.  **Configure the Project:**
    * Copy your S3 bucket name into the `config.ini` file.

4.  **Install Dependencies & Run:**
    * Create and activate a Python virtual environment:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * Install the required libraries:
        ```bash
        pip install -r requirements.txt
        ```
    * Run the Flask server in debug mode:
        ```bash
        flask --app application --debug run
        ```
5.  **View the App:** Open **`http://localhost:5000`** in your browser.