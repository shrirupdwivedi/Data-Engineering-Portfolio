<img src="https://github.com/user-attachments/assets/beffea24-6d1f-479c-9a65-8aace3e52d92" alt="image" width="300"/>

# 📈 Databricks Stock Trade/Quote Pipeline

An end-to-end data engineering project that simulates the ingestion, deduplication, and analytical enrichment of stock trade and quote data using **Databricks**, **Delta Lake**, and **Lakehouse architecture** (Bronze → Silver → Gold).

---

## 🚀 Project Overview

This pipeline mimics a real-time data platform used in financial trading systems. It ingests trade and quote events in CSV/JSON format, deduplicates records using event keys and arrival time, and enriches quote records with analytical context such as:

- Latest trade price before each quote
- 30-minute moving average of trade price before each quote
- Bid/ask price movement from the previous day's closing trade

---

## 🧰 Tech Stack

- **Databricks (AWS)**
- **Apache Spark (PySpark + SQL)**
- **Delta Lake** – schema evolution, MERGE INTO, Z-Ordering
- **Unity Catalog Volumes** – for file ingestion
- **Databricks Workflows** – to orchestrate Bronze → Silver → Gold

---

## 🧱 Architecture

- **Bronze Layer**: Ingest and parse raw CSV/JSON
- **Silver Layer**: Deduplicate and `MERGE INTO` cleaned trade/quote tables
- **Gold Layer**: Enrich quote records with historical + analytical features

---

## 🗃️ Data Model


- Unique keys: `trade_dt`, `symbol`, `event_tm`, `exchange`, `event_seq_nb`
- Partitioned tables for performance
- Normalized event schema with derived analytical fields

---

## 🔄 Pipeline Breakdown

### 🔹 Bronze: Raw Ingestion
- Source files uploaded into Unity Catalog volume (`/Volumes/capstone/default/csv/`)
- Records are parsed using custom `parse_csv()` and `parse_json()` logic
- Invalid records flagged with `rec_type = 'B'`

### 🔹 Silver: Deduplication
- Composite key used to identify unique events
- Uses `ROW_NUMBER()` over arrival time to pick latest version
- `MERGE INTO` applied to `trade_data` and `quote_data` Delta tables

### 🔹 Gold: Analytical Enrichment
- 30-min moving average trade price using `WINDOW + RANGE` function
- `LAST_VALUE(..., TRUE)` to populate latest trade context for each quote
- Joins with prior day's close to calculate price delta
- Outputs to: `/Volumes/capstone/default/quote_analytics/date=YYYY-MM-DD`

---

## ⚙️ How to Run (via Databricks Workflow)

- Run notebooks in this order:
  1. `1_ingest_bronze.py`
  2. `2_merge_silver.py`
  3. `3_enrich_gold.py`
- Orchestrate them in `Databricks Workflows` as a DAG
- Use `dbutils.widgets.get("trade_date")` to make the pipeline dynamic per day

---

## 📌 Key Features

- ✅ Late-arriving data support with upserts
- ✅ 30-minute rolling window logic
- ✅ Delta schema evolution + partitioning
- ✅ Optimized joins with broadcast hints
- ✅ Gold table ready for analytics and ML

---

## 💡 Learnings

- Writing robust ingestion logic in PySpark
- Using SQL window functions for time-sequence enrichment
- Best practices for MERGE INTO, Z-Ordering, and Delta architecture
- Automating multi-layer pipelines with Databricks Jobs

---



