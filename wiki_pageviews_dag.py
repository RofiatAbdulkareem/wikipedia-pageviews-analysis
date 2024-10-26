import requests
import gzip
import pandas as pd
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set default arguments
default_args = {
    'owner': 'rofiat',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 10),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    dag_id="wikipedia_pageviews_dags",
    description="Wikipedia pageviews",
    default_args=default_args,
    schedule_interval="@once",
)

# To download the pageviews i.e., fetching the raw data
def download_pageviews(**kwargs):
    url = 'https://dumps.wikimedia.org/other/pageviews/2024/2024-10/pageviews-20241010-160000.gz'
    response = requests.get(url, stream=True, verify=False)
    file_path = '/tmp/pageviews-20241010-160000.gz'
    with open(file_path, 'wb') as f:
        f.write(response.content)
    return file_path

# Extracting the gz file
def extract_gz_file(ti):
    file_path = ti.xcom_pull(task_ids='download_pageviews')
    extracted_file_path = file_path.replace('.gz', '')

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with gzip.open(file_path, 'rb') as f_in, open(extracted_file_path, 'wb') as f_out:
            f_out.write(f_in.read())

    except (FileNotFoundError, gzip.BadGzipFile) as e:
        logger.error(f"Error during extraction: {e}")
        raise

    return extracted_file_path

# For data filtering
def filter_data(ti):
    file_path = ti.xcom_pull(task_ids='extract_gz_file')
    selected_companies = ['Amazon', 'Apple', 'Facebook', 'Google', 'Microsoft']
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            fields = line.split()
            if len(fields) > 3 and any(company.lower() in fields[0].lower() for company in selected_companies):
                data.append((fields[0], int(fields[2])))
    return data

# Load to Postgres using SQLAlchemy
def load_to_db(ti):
    data = ti.xcom_pull(task_ids='filter_data')

    # Create SQLAlchemy engine
    engine = create_engine('postgresql+psycopg2://postgres:oyizam@localhost:5432/capstone_project')

    # Convert the data into a DataFrame and load it into the database
    df = pd.DataFrame(data, columns=['company', 'pageviews'])

    logger.info(f"DataFrame shape: {df.shape}")
    logger.info(f"DataFrame preview: {df.head()}")

    # Write the DataFrame to PostgreSQL table
    try:
        with engine.connect() as connection:
            df.to_sql('pageviews', connection, if_exists='replace', index=False)
        logger.info("Data loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading data to database: {str(e)}")
    finally:
        engine.dispose()

# Analyze data from Postgres
def analyze_data():
    # Create SQLAlchemy engine
    engine = create_engine('postgresql+psycopg2://postgres:oyizam@localhost:5432/capstone_project')
    
    try:
        # Read data from PostgreSQL using pandas
        df = pd.read_sql('SELECT * FROM pageviews', con=engine)
        
        # Perform analysis: finding the company with the highest pageviews
        result = df.groupby('company')['pageviews'].sum().idxmax()
        
        # Output the result
        logger.info(f'Company with the highest pageviews: {result}')
        
    except Exception as e:
        logger.error(f"Error analyzing data: {str(e)}")
    finally:
        engine.dispose()

# Define the tasks
t1 = PythonOperator(
    task_id='download_pageviews',
    python_callable=download_pageviews,
    dag=dag,
)

t2 = PythonOperator(
    task_id='extract_gz_file',
    python_callable=extract_gz_file,
    dag=dag,
)

t3 = PythonOperator(
    task_id='filter_data',
    python_callable=filter_data,
    dag=dag,
)

t4 = PythonOperator(
    task_id='load_to_db',
    python_callable=load_to_db,
    dag=dag,
)

t5 = PythonOperator(
    task_id='analyze_data',
    python_callable=analyze_data,
    dag=dag,
)

# Task dependencies
t1 >> t2 >> t3 >> t4 >> t5
