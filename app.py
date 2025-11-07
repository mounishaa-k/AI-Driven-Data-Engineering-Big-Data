import streamlit as st
import pandas as pd
import numpy as np
import re
import os
import io
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords

# ----------------------- Setup -----------------------
st.set_page_config(page_title='E-commerce Fake Review Detector', layout='wide')
st.title('🧱 Data Engineering (Airflow) + 🧠 Fake Review Detection Dashboard')

# Ensure stopwords
try:
    nltk.data.find('corpora/stopwords')
except Exception:
    nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words('english'))

# ----------------------- Data Cleaning Helper -----------------------
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

# ----------------------- Model Training -----------------------
def train_model(df, text_col='review_text', label_col='label'):
    X = df[text_col].fillna('').astype(str).apply(clean_text)
    y = df[label_col].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_features=20000)),
        ('clf', LogisticRegression(max_iter=1000))
    ])
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    report = classification_report(y_test, preds, output_dict=True)
    acc = accuracy_score(y_test, preds)
    cm = confusion_matrix(y_test, preds)
    return pipeline, report, acc, cm

# ----------------------- Confusion Matrix Plot -----------------------
def make_confusion_heatmap(cm, ax):
    TN, FP = cm[0,0], cm[0,1]
    FN, TP = cm[1,0], cm[1,1]
    total = cm.sum()
    labels = np.array([["TN", "FP"], ["FN", "TP"]])
    annot = [[f"{labels[i][j]}\n{cm[i,j]}\n{100*cm[i,j]/total:.1f}%" for j in range(2)] for i in range(2)]
    sns.heatmap(cm, annot=annot, fmt='', cmap="Blues", cbar=False, ax=ax, linewidths=0.5)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    ax.set_title("Confusion Matrix", fontsize=10)

# ----------------------- Data Engineering Summary -----------------------
METADATA_PATH = "/tmp/etl_metadata.json"

def show_data_engineering_summary():
    st.header("📊 Data Engineering Pipeline Summary (Airflow Output)")
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r') as f:
            meta = json.load(f)

        st.json(meta)

        # Safely extract numeric values for display
        raw_rows = int(meta.get("raw_rows", 0))
        cleaned_rows = int(meta.get("cleaned_rows", 0))
        missing_removed = int(meta.get("missing_before", 0))

        col1, col2, col3 = st.columns(3)
        col1.metric("Raw Rows", raw_rows)
        col2.metric("Cleaned Rows", cleaned_rows)
        col3.metric("Missing Removed", missing_removed)

        st.caption(f"📅 Last ETL Run: {meta.get('extract_time', 'N/A')}")
        st.info(f"✅ Cleaned data saved at: `{meta.get('cleaned_data_path', 'N/A')}`")

        # Bar chart for data counts
        counts = pd.DataFrame({
            "Stage": ["Raw Data", "Cleaned Data"],
            "Records": [raw_rows, cleaned_rows]
        })
        st.bar_chart(counts.set_index("Stage"))
    else:
        st.warning("⚠️ No ETL metadata found. Run your Airflow ETL DAG first to generate `/tmp/etl_metadata.json`.")

# ----------------------- Sidebar -----------------------
st.sidebar.header('Quick Actions')

# Upload pretrained model
pretrained_model_file = st.sidebar.file_uploader('Upload pretrained pipeline', type=['pkl', 'joblib'])
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
if pretrained_model_file is not None:
    try:
        uploaded_bytes = io.BytesIO(pretrained_model_file.read())
        st.session_state.pipeline = joblib.load(uploaded_bytes)
        st.sidebar.success("✅ Pretrained model loaded successfully.")
    except Exception as e:
        st.sidebar.error(f"Error loading model: {e}")

# Text prediction
input_text = st.sidebar.text_area('Enter review text to classify', height=150)
if st.sidebar.button('Predict'):
    if not input_text.strip():
        st.sidebar.error('Please enter text.')
    elif st.session_state.pipeline is None:
        st.sidebar.error('No model found. Train or upload one first.')
    else:
        cleaned = clean_text(input_text)
        pred = st.session_state.pipeline.predict([cleaned])[0]
        proba = st.session_state.pipeline.predict_proba([cleaned])[0]
        label_str = "Fake" if int(pred)==1 else "Real"
        st.sidebar.success(f"Prediction: **{label_str}**")
        st.sidebar.info(f"Probabilities → Real: {proba[0]*100:.2f}%, Fake: {proba[1]*100:.2f}%")

# ----------------------- Main -----------------------
st.markdown("---")
show_data_engineering_summary()
st.markdown("---")
st.header("🧠 Machine Learning Model Training & Evaluation")

uploaded_file = st.file_uploader('Upload Cleaned Dataset (from Airflow)', type=['csv'])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())
    text_col = st.text_input('Text column name', 'review_text')
    label_col = st.text_input('Label column name', 'label')
    if st.button('Train model'):
        with st.spinner('Training...'):
            pipeline, report, acc, cm = train_model(df, text_col, label_col)
            st.session_state.pipeline = pipeline
            st.success(f"✅ Model trained — Accuracy: {acc*100:.2f}%")
            st.subheader("Classification Report")
            cr_df = pd.DataFrame(report).transpose()
            st.table(cr_df)
            fig, ax = plt.subplots(figsize=(3,3))
            make_confusion_heatmap(cm, ax)
            st.pyplot(fig)
            joblib.dump(pipeline, 'fake_review_pipeline.joblib')
            with open('fake_review_pipeline.joblib', 'rb') as f:
                st.download_button('⬇️ Download Trained Model', data=f, file_name='fake_review_pipeline.joblib')
