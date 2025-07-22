# HR Analytics Dashboard

An interactive data dashboard designed to simulate a simplified end-to-end data pipeline, from data ingestion to visualization, using modern Python tools.

This project demonstrates practical data engineering and analysis skills by processing an HR dataset focused on job changes in the Data Science field.
Dataset: Kaggle - HR Analytics: Job Change of Data Scientists

---

## Project Objectives

- Build a modular ETL pipeline with Python and SQL
- Clean and structure raw CSV data using Pandas
- Store transformed data in a SQLite relational database
- Query with SQL for aggregation and business insights
- Visualize trends interactively using Streamlit and Plotly
- (Planned) Dockerize the app for deployment
- (Planned) Connect to BigQuery or GCS for cloud simulation
- (Planned) Add DAG simulation via Apache Airflow (local)

---

## Tech Stack

| Layer            | Tools Used                          |
|------------------|-------------------------------------|
| Programming      | Python                              |
| Data Handling    | Pandas, JSON                        |
| Database         | SQLite (TBD BigQuery)       |
| Query Language   | SQL (CTEs, aggregations, window fx) |
| Orchestration    | (Planned) Airflow (Local DAG)     |
| Visualization    | Streamlit, Plotly                   |
| Deployment       | (Planned) Docker                  |
| Cloud Simulation | (Planned) GCP Free Tier           |

---

## Workflow Overview

```mermaid
graph TD;
A[Raw CSV Data] --> B[Pandas Cleaning];
B --> C[SQLite Database];
C --> D[SQL Queries];
D --> E[Streamlit Dashboard];
F[Optional GCP Upload] --> C;
G[Optional Airflow DAG] --> B;
