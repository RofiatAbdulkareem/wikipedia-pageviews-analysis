# Data Pipeline Documentation: Wikipedia Pageviews Analysis

## 1. Introduction
The **Wikipedia Pageviews Analysis** project aims to collect, process, and analyze Wikipedia pageviews for major tech companies, including **Amazon**, **Apple**, **Facebook**, **Google**, and **Microsoft**. This project uses **Apache Airflow** for orchestrating the data pipeline, which allows for scheduling, monitoring, and managing data workflows efficiently. The insights generated from this analysis can be valuable for understanding user engagement trends.

## 2. Pipeline Design

### Data Flow
The data pipeline consists of the following steps:

1. **Download**: The pipeline initiates with the `download_pageviews` task, which fetches compressed pageview data from Wikimedia.
2. **Extract**: The `extract_gz_file` task extracts the gzipped file to access the raw pageview data.
3. **Filter**: The `filter_data` task processes the extracted data, filtering for selected companies and storing relevant pageviews.
4. **Load**: The `load_to_db` task loads the filtered data into a **PostgreSQL** database using **SQLAlchemy**.
5. **Analyze**: The `analyze_data` task performs analysis on the database, querying to find the company with the highest pageviews.

### 3. DAG Structure
The Directed Acyclic Graph (DAG) for this project is structured as follows:
- **DAG ID**: `wikipedia_pageviews_dags`
- **Tasks**: 
  - `download_pageviews`
  - `extract_gz_file`
  - `filter_data`
  - `load_to_db`
  - `analyze_data`
- **Task Dependencies**: Each task is executed sequentially, with dependencies ensuring the flow of data from one step to the next.

### Database Choice: **PostgreSQL**
**PostgreSQL** was chosen as the database for the following reasons:
- **Robustness**: PostgreSQL is a powerful, open-source relational database system known for its robustness and support for advanced data types.
- **Scalability**: It can handle large datasets, making it suitable for processing potentially massive amounts of pageview data.
- **SQL Support**: Its support for SQL allows for complex queries, making analysis straightforward.


## Conclusion
The **Wikipedia Pageviews Analysis** pipeline is a robust solution for analyzing user engagement trends among major tech companies. The use of **Apache Airflow** for orchestration ensures that the pipeline is efficient, scalable, and maintainable. The decisions made regarding database choice and task management reflect best practices in data engineering, enabling effective data processing and analysis.
