# Porsche 911 Market Intelligence

An educational end-to-end data analytics project focused on collecting, storing and analyzing Porsche 911 listings from an online automotive marketplace.

The project combines **Python, web scraping, data modeling, SQLite, SQL and Power BI** to build a small Market Intelligence platform capable of exploring market structure, asking prices, vehicle specifications and historical listing dynamics.

The goal is not simply to build a scraper or a dashboard, but to demonstrate how a technical manager can design and implement a complete data product — from automated data acquisition and data quality controls to analytical data modeling and business-oriented reporting.

> **Project status:** The Python data pipeline and analytical database are implemented. The first Power BI dashboard MVP is complete. Historical data collection is ongoing.

---

## 🎯 Project objectives

The project aims to answer questions such as:

- What does the Porsche 911 listing market currently look like?
- How is the market segmented by generation, model, version and technical characteristics?
- What are the typical asking prices across different segments?
- How do asking prices and listing volumes evolve over time?
- How do mileage, model year and vehicle specifications relate to asking prices?
- How frequently do sellers adjust their asking prices?
- How long do listings remain observable in the collected market data?

The analytical questions are defined before building the dashboard to keep the analysis focused on meaningful business questions rather than simply visualizing available data.

---

## 🏗️ Solution architecture

The project follows an end-to-end data pipeline:

```text
Online Automotive Marketplace
            │
            ▼
      Python Scraper
            │
            ├── Light Crawl
            │      └── Listing snapshots
            │
            └── Heavy Crawl
                   └── Detailed vehicle attributes
            │
            ▼
   Data Validation & Normalization
            │
            ▼
       SQLite Database
            │
            ├── Historical snapshots
            ├── Vehicle details
            ├── Scraper run information
            └── Exchange rates
            │
            ▼
      SQL Analytical Views
            │
            ▼
         CSV Export
            │
            ▼
         Power BI
            │
            ▼
  Porsche 911 Market Intelligence
```

The current implementation uses SQLite as the analytical database and CSV files as a simple local integration layer between SQLite and Power BI.

---

## 📂 Project components

### 1. Data Acquisition — Python

Automated collection and processing of Porsche 911 listings.

Key capabilities:

- Web scraping using Requests and BeautifulSoup.
- Two-stage data acquisition: light crawl and heavy crawl.
- Historical listing snapshots.
- Structured data modeling with Python dataclasses.
- Data validation, normalization and quality monitoring.
- Duplicate detection and advert ID consistency checks.
- SQLite database operations.
- SQL analytical views.
- CSV export for Power BI.
- Exchange rate retrieval from the NBP API.

📘 **Detailed documentation:** [Data Acquisition README](./data_acquisition/README.md)

> Update the path if your Python project folder has a different name.

### 2. Dashboard — Power BI

An interactive dashboard designed to explore the Porsche 911 listing market from multiple analytical perspectives.

The current MVP consists of four report pages:

- Market Overview
- Generation Drill Through
- Price Dynamics
- Listing Lifecycle

The report combines market-level KPIs, segmentation, price analysis, vehicle characteristics and historical listing observations.

📊 **Detailed documentation:** [Power BI Dashboard README](./power-bi-analytics/README.md)

> Update the path if your Power BI folder has a different name.

---

## 🛠️ Technology stack

| Area | Technology |
|---|---|
| Programming | Python |
| Web scraping | Requests, BeautifulSoup |
| Data structures | Python dataclasses |
| Database | SQLite |
| Database access | Python `sqlite3` |
| Analytical layer | SQL |
| Data processing | Pandas |
| Data exchange | CSV |
| Business Intelligence | Microsoft Power BI |
| Data transformation | Power Query |
| Calculations | DAX |
| Exchange rates | NBP API |
| Version control | Git / GitHub |

---

## 💡 Skills demonstrated

### 🐍 Python & Automation
- Object-oriented programming and class-based architecture.
- Building a modular data acquisition pipeline.
- HTML parsing and web scraping.
- Working with external APIs.
- Data structures, type hints and dataclasses.
- Exception handling, logging and operational monitoring.

### 🗄️ Data Engineering Fundamentals
- Relational data modeling.
- Designing SQLite tables and primary keys.
- Separating historical observations from vehicle attributes.
- Data persistence and idempotent snapshot insertion.
- SQL views and reusable analytical logic.
- ETL pipeline orchestration.
- Data quality checks and validation.

### 📊 Business Intelligence & Analytics
- Power BI data modeling.
- Power Query data transformation.
- DAX calculations and KPI development.
- Market segmentation and exploratory analysis.
- Interactive reporting and drill-through navigation.
- Translating business questions into analytical requirements.

### 🧠 Analytical Thinking
- Defining analytical questions before designing visualizations.
- Understanding the limitations of observational data.
- Distinguishing asking prices from transaction prices.
- Separating observed listing duration from confirmed time to sale.
- Building a foundation for future statistical analysis and comparable-vehicle analysis.

---

## 📈 Dashboard pages

The Power BI report currently contains:

1. **Market Overview** — overall market structure, prices, listing volumes and geographical distribution.
2. **Generation Drill Through** — detailed analysis of a selected generation and its technical characteristics.
3. **Price Dynamics** — historical asking-price trends and seller price adjustments.
4. **Listing Lifecycle** — observed listing duration and its relationship with generations and prices.

[Dashboard screenshots and detailed descriptions →](./power-bi-analytics/README.md)

---

## 🎓 Project background

This is an educational and portfolio project created to develop practical skills at the intersection of:

- Data Analytics
- Python Programming
- SQL
- Business Intelligence
- Automation
- Data Engineering Fundamentals
- Market Intelligence

The Porsche 911 market is used as a practical domain for developing these capabilities.

The project deliberately connects business questions with technical implementation:

```text
Business Question
       ↓
Data Acquisition
       ↓
Data Model
       ↓
Data Quality
       ↓
Analytical Logic
       ↓
BI Model
       ↓
Dashboard
       ↓
Business Insight
```

---

## 🚀 Current milestone

The project has reached its first end-to-end milestone:

- [x] Automated data collection
- [x] Historical listing snapshots
- [x] Detailed vehicle data
- [x] SQLite database
- [x] Data quality monitoring
- [x] SQL analytical views
- [x] CSV export
- [x] Power BI data model
- [x] Interactive dashboard MVP
- [x] Market segmentation analysis
- [x] Asking-price and market dynamics analysis

The next iteration will focus on increasing analytical depth as more historical observations are collected.

---

## 🔭 Future development

Potential future directions include:

- Comparable-vehicle analysis.
- More advanced statistical analysis.
- Further development of historical market insights.
- Potential machine learning applications.

These are future development ideas, not implemented features.

---

## 📌 Project philosophy

> **Good analytics starts with good questions and a reliable data pipeline.**

The dashboard is the final layer of the system, not the starting point.

The objective is to build a small but complete Market Intelligence platform that collects market data and turns it into structured information that can be explored, compared and analyzed over time.

