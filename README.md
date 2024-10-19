# Wikipedia Pageviews Analysis

## Overview
This project aims to analyze Wikipedia pageviews for major tech companies, providing insights into user engagement and trends over time. The data is fetched from Wikimedia, processed, and stored in a PostgreSQL database for analysis.

## Requirements
- **Python**: 3.x
- **Apache Airflow**
- **PostgreSQL**
- **Required Python libraries**: 
  - `requests`
  - `pandas`
  - `sqlalchemy`
  - `gzip`
  - `airflow`
  
To install the required libraries, create a `requirements.txt` file with the following content:
requests pandas sqlalchemy gzip apache-airflow

bash
Copy code

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/wikipedia-pageviews-analysis.git
   cd wikipedia-pageviews-analysis
Install the Requirements:

bash
Copy code
pip install -r requirements.txt
Set Up PostgreSQL Database:

sql
Copy code
CREATE DATABASE capstone_project;
Running the Project
Start Airflow:

bash
Copy code
airflow scheduler &
airflow webserver -p 8080
Access the Airflow Web UI: Open your browser and go to http://localhost:8080.

Trigger the DAG: Locate the wikipedia_pageviews_dags in the Airflow UI and trigger it to start the data pipeline.

Pipeline Documentation
For a detailed explanation of the pipeline architecture and design, see pipeline_documentation.md.

Simple Analysis
The final task in the DAG queries the database to determine which of the five companies had the highest pageviews. The SQL query used is:

sql
Copy code
SELECT company, MAX(pageviews) AS max_pageviews
FROM pageviews
GROUP BY company
ORDER BY max_pageviews DESC
LIMIT 1;
