from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import re
import os
import json
import nltk
from nltk.corpus import stopwords

# -------------------------------------------
# SETUP
# -------------------------------------------
nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words('english'))

CLEANED_DATA_PATH = "/tmp/cleaned_reviews.csv"
RAW_DATA_PATH = "/tmp/raw_kaggle_dataset.csv"
TRANSFORMED_PATH = "/tmp/transformed.csv"
METADATA_PATH = "/tmp/etl_metadata.json"
KAGGLE_DATASET = "mexwell/fake-reviews-dataset"

# -------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------
def clean_text(text):
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [t for t in text.split() if t not in STOPWORDS and len(t) > 1]
    return " ".join(tokens)


# -------------------------------------------
# EXTRACT
# -------------------------------------------
def extract():
    print("📦 Extracting Kaggle dataset...")
    os.system(f"kaggle datasets download -d {KAGGLE_DATASET} -p /tmp --unzip")

    # Find the downloaded CSV
    for file in os.listdir("/tmp"):
        if file.lower().endswith(".csv") and "fake" in file.lower():
            os.rename(f"/tmp/{file}", RAW_DATA_PATH)
            print(f"✅ Dataset saved at {RAW_DATA_PATH}")
            break

    df_raw = pd.read_csv(RAW_DATA_PATH)
    print(f"🔍 First 5 rows of raw dataset:\n{df_raw.head()}")


# -------------------------------------------
# TRANSFORM
# -------------------------------------------
def transform():
    print("⚙ Transforming and cleaning Kaggle dataset...")
    df = pd.read_csv(RAW_DATA_PATH)

    # Ensure required columns exist
    if 'text_' not in df.columns or 'label' not in df.columns:
        raise ValueError(f"Dataset columns not found! Found columns: {df.columns.tolist()}")

    df = df[['text_', 'label']].rename(columns={'text_': 'review_text', 'label': 'label'})

    # Convert labels (CG → 1, OR → 0)
    df['label'] = df['label'].astype(str).apply(lambda x: 1 if x.strip().upper() == 'CG' else 0)

    # Count missing values before cleaning
    missing_before = int(df.isna().sum().sum())

    # Clean review text
    df['review_text'] = df['review_text'].astype(str).apply(clean_text)

    # Drop duplicates and missing entries
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # Save transformed dataset
    df.to_csv(TRANSFORMED_PATH, index=False)
    print(f"✅ Transformed dataset saved to {TRANSFORMED_PATH} with {len(df)} rows")
    print("🔍 First 5 rows:\n", df.head())

    # Save ETL metadata
    try:
        meta = {
            "extract_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "raw_rows": int(pd.read_csv(RAW_DATA_PATH).shape[0]),
            "cleaned_rows": int(df.shape[0]),
            "missing_before": missing_before,
            "pipeline_status": "SUCCESS",
            "cleaned_data_path": CLEANED_DATA_PATH,
            "raw_data_path": RAW_DATA_PATH
        }
        with open(METADATA_PATH, "w") as f:
            json.dump(meta, f, indent=4)
        print(f"✅ Metadata saved at {METADATA_PATH}")
    except Exception as e:
        print(f"⚠️ Could not save metadata: {e}")


# -------------------------------------------
# LOAD
# -------------------------------------------
def load():
    print("💾 Loading final cleaned dataset...")
    df = pd.read_csv(TRANSFORMED_PATH)
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"✅ Final dataset saved at {CLEANED_DATA_PATH}")
    print("🔍 First 5 rows of final dataset:\n", df.head())


# -------------------------------------------
# DAG DEFINITION
# -------------------------------------------
default_args = {
    "owner": "mounisha",
    "start_date": datetime(2025, 10, 25)
}

with DAG(
    dag_id="kaggle_cleaning_etl_pipeline",
    default_args=default_args,
    description="ETL pipeline for Kaggle fake reviews dataset (with cleaning and metadata)",
    schedule_interval=None,
    catchup=False,
) as dag:

    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    transform_task = PythonOperator(task_id="transform", python_callable=transform)
    load_task = PythonOperator(task_id="load", python_callable=load)

    extract_task >> transform_task >> load_task
