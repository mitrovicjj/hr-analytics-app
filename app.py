import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

conn = sqlite3.connect("job_data.db")

st.title("HR Analytics Dashboard 📊")

query_option = st.selectbox("Izaberi analizu:", [
    "Prosječna plata po gradu i obrazovanju",
    "Promjena posla po godinama iskustva",
    "Koliko ljudi sa MSc/PhD mijenja posao",
    "Sati obuke po gradu i stepenu obrazovanja",
    "Distribucija kandidata koji zele promijeniti posao, po tipu kompanije"
])

df = pd.DataFrame()

if query_option == "Prosječna plata po gradu i obrazovanju":
    query = """
    SELECT city, education_level, ROUND(AVG(training_hours), 2) AS avg_training_hours
    FROM candidates
    GROUP BY city, education_level
    ORDER BY avg_training_hours DESC
    """
    df = pd.read_sql_query(query, conn)
    st.write(df.head(10))
    fig = px.bar(df.head(10), x='city', y='avg_training_hours', color='education_level', title="Top 10 gradova po trening satima")
    st.plotly_chart(fig)

elif query_option == "Promjena posla po godinama iskustva":
    query = """
    SELECT 
        experience,
        COUNT(*) AS total_people,
        SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS changed_jobs,
        ROUND(SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 2) AS change_ratio
    FROM candidates
    GROUP BY experience
    ORDER BY experience
    """
    df = pd.read_sql_query(query, conn)
    st.write(df)
    fig = px.line(df, x='experience', y='change_ratio', title="Stopa promene posla po iskustvu")
    st.plotly_chart(fig)

elif query_option == "Koliko ljudi sa MSc/PhD mijenja posao":
    query = """
    SELECT education_level,
           COUNT(*) AS total,
           SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS looking_for_change,
           ROUND(SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 2) AS change_ratio
    FROM candidates
    WHERE education_level IN ('Masters', 'Phd')
    GROUP BY education_level
    """
    df = pd.read_sql_query(query, conn)
    st.write(df)
    fig = px.bar(df, x='education_level', y='change_ratio', title="Promena posla kod MSc/PhD kandidata")
    st.plotly_chart(fig)

elif query_option == "Sati obuke, po gradu i stepenu obrazovanja":
    query = """
    SELECT 
        city,
        education_level,
        ROUND(AVG(training_hours), 2) AS avg_training_hours
    FROM 
        candidates
    GROUP BY 
        city, education_level
    ORDER BY 
        avg_training_hours DESC
    """
    df = pd.read_sql_query(query, conn)
    st.write(df.head(10))
    fig = px.bar(df.head(10), x='city', y='avg_training_hours', color='education_level', title="Trening sati (top 10 kombinacija)")
    st.plotly_chart(fig)

elif query_option == "Distribucija kandidata koji zele promijeniti posao, po tipu kompanije":
    query = """
    SELECT company_type,
           COUNT(*) AS total,
           SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS looking_for_change
    FROM candidates
    GROUP BY company_type
    """
    df = pd.read_sql_query(query, conn)
    df["change_ratio"] = (df["looking_for_change"] / df["total"]).round(2)
    st.write(df)
    fig = px.bar(df, x='company_type', y='change_ratio', title="Stopa promene po tipu kompanije")
    st.plotly_chart(fig)

conn.close()