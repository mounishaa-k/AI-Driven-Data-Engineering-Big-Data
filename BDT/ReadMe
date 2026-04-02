# 🚀 End-to-End Big Data Engineering Pipeline for E-Commerce Analytics

## 📌 Overview

This project demonstrates a complete end-to-end **Big Data Engineering pipeline** built using **Microsoft Azure** services. The system ingests data from multiple sources, processes it using distributed computing, and prepares it for analytics using a **Medallion (Lakehouse) Architecture**.

---

## 🏗️ Architecture

![Architecture Diagram](ArchitectureDiagram.png)

---

## ⚙️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Azure Data Factory (ADF)** | Data ingestion & orchestration |
| **Azure Data Lake Storage Gen2 (ADLS)** | Scalable storage |
| **Azure Databricks (Apache Spark)** | Distributed data processing |
| **Azure Synapse Analytics** | Querying & analytics |
| **Python (PySpark)** | Data transformation |

---

## 🔄 Data Pipeline Flow

### 1️⃣ Data Ingestion
- **Sources:** HTTP (GitHub), SQL Database
- **Tool:** Azure Data Factory
- **Feature:** Parameterized pipelines + ForEach loop

![ADF Ingestion Pipeline](AzureDataFactory_IngestionPipeline.png)

### 2️⃣ Bronze Layer (Raw Data)
- Stores raw, unprocessed data in ADLS

![Bronze Layer](BronzeLayer.png)

### 3️⃣ Data Transformation (Databricks)
- Data cleaning, transformation, and joins
- Distributed processing using Apache Spark

![Data Transformation](DataTransformation.png)

### 4️⃣ Silver Layer (Processed Data)
- Cleaned and structured data ready for analytics

![Silver Layer](SilverLayer%20.png)

### 5️⃣ Analytics using Synapse
- External tables
- SQL queries using schema-on-read

![Azure Synapse Analytics](AzureSynapseAnalytics.png)

### 6️⃣ Gold Layer (Serving Layer)
- Aggregated business insights
- Ready for reporting and dashboards

![Gold Layer](GoldLayer.png)

---

## 🧠 Key Concepts Used

- 🏅 Medallion Architecture (Bronze → Silver → Gold)
- ⚙️ Parameterized Data Ingestion
- ⚡ Distributed Processing (Apache Spark)
- 🔗 Data Enrichment
- 📖 Schema-on-read
- 🏠 Data Lakehouse Architecture

---

## 📂 Project Structure
```
BDT/
│
├── ArchitectureDiagram.png
├── ADLSGen2_Data_Lake.png
├── AzureDataFactory_IngestionPipeline.png
├── AzureSynapseAnalytics.png
├── AzureSynapse_sql code.txt
├── BronzeLayer.png
├── SilverLayer .png
├── GoldLayer.png
├── DataTransformation using DataBricks.ipynb
├── DataTransformation.png
├── ActivityDiagram.jpeg
├── airflow_cleaning_dag.py
├── app.py
├── requirements.txt
└── ReadMe
```

---

## ▶️ How to Run

1. **Create Azure resources:**
   - Azure Data Factory
   - Azure Data Lake Storage Gen2
   - Azure Databricks
   - Azure Synapse Analytics

2. Run the **ADF pipeline** for data ingestion
3. Execute the **Databricks notebook** (`DataTransformation using DataBricks.ipynb`) for transformation
4. Query the processed data using **Synapse** (refer to `AzureSynapse_sql code.txt`)

---

## 📊 UML / Workflow Diagram

![Activity Diagram](ActivityDiagram.jpeg)

---

## 📌 Current Status

| Component | Status |
|-----------|--------|
| Data Ingestion (ADF - Parameterized Pipelines) | ✅ Done |
| Bronze Layer Storage | ✅ Done |
| Data Transformation (Databricks - Spark) | ✅ Done |
| Silver Layer | ✅ Done |
| Synapse Query Layer | ✅ Done |
| Gold Layer (Serving) | ✅ Done |

---

## 🔮 Future Enhancements

- [ ] Real-time ingestion using Event Hubs
- [ ] Integration with Power BI dashboards
- [ ] Data quality monitoring
- [ ] CI/CD pipeline for deployment

---

## 👩‍💻 Author

**K Mounisha**  
🔗 GitHub: [mounishaa-k](https://github.com/mounishaa-k)

---

## ⭐ Key Highlight

> This project simulates a **real-world enterprise data engineering pipeline**, covering ingestion, transformation, enrichment, and analytics using scalable cloud technologies.
