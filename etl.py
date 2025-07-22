import pandas as pd
import sqlite3
import os

def load_data(csv_path):
    return pd.read_csv(csv_path)

def drop_duplicates(df):
    return df.drop_duplicates()

def drop_unused_columns(df):
    return df.drop(columns=["enrollee_id"], errors="ignore")

def clean_missing_and_transform(df):
    df = df.copy()
    # fill na
    df["gender"] = df["gender"].fillna("Other")
    df["enrolled_university"] = df["enrolled_university"].fillna("no_enrollment")
    df["education_level"] = df["education_level"].fillna("Other")
    df["major_discipline"] = df["major_discipline"].fillna("Other")
    df["experience"] = df["experience"].fillna("0")
    df["company_type"] = df["company_type"].fillna("Other")
    df["last_new_job"] = df["last_new_job"].fillna("never")

    # normalize experience
    df["experience"] = df["experience"].astype(str)
    df["experience"] = df["experience"].str.replace(">", "", regex=False)
    df["experience"] = df["experience"].str.replace("<", "", regex=False)
    df["experience"] = df["experience"].replace({'>20': '20', '<1': '0', ' nan': '0'})
    df["experience"] = pd.to_numeric(df["experience"], errors='coerce').fillna(0).astype(int)

    # bin experience
    df["experience"] = df["experience"].apply(bin_experience)
    df["experience"] = df["experience"].map({
        "No experience": 0,
        "Junior": 1,
        "Mid-level": 2,
        "Senior": 3,
        "Experienced": 4,
        "Veteran": 5
    })

    # company size- ordinal encoding + fill na
    size_map = {
        '<10': 0,
        '10/49': 1,
        '50-99': 2,
        '100-500': 3,
        '500-999': 4,
        '1000-4999': 5,
        '5000-9999': 6,
        '10000+': 7
    }
    df["company_size"] = df["company_size"].map(size_map).fillna(0)

    return df

def bin_experience(val):
    if val == 0:
        return "No experience"
    elif val <= 3:
        return "Junior"
    elif val <= 6:
        return "Mid-level"
    elif val <= 10:
        return "Senior"
    elif val <= 15:
        return "Experienced"
    else:
        return "Veteran"

def full_clean_pipeline(csv_path):
    df = load_data(csv_path)
    df = drop_duplicates(df)
    df = drop_unused_columns(df)
    df = clean_missing_and_transform(df)
    return df

def write_to_sqlite(df, db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql("candidates", conn, if_exists="replace", index=False)
    conn.close()

if __name__ == "__main__":
    cleaned_df = full_clean_pipeline("data/hr_data.csv")
    write_to_sqlite(cleaned_df, "database/job_data.db")