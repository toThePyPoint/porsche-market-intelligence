# Porsche 911 Market Intelligence — Power BI Dashboard

The Power BI dashboard is the analytical layer of the Porsche 911 Market Intelligence project.

It transforms the data collected by the Python pipeline into an interactive reporting tool for exploring market structure, asking prices, vehicle characteristics and historical listing dynamics.

The dashboard is built around defined analytical questions rather than simply displaying available data.

> **Status:** First working MVP completed. Historical data collection is ongoing.

---

## 🎯 Dashboard Objectives

The report is designed to help answer questions such as:

- What does the observed Porsche 911 listing market look like?
- How are asking prices distributed?
- How do asking prices differ across generations and versions?
- How do model year and mileage relate to asking prices?
- How are Porsche 911 listings distributed geographically?
- How do sellers adjust their asking prices over time?
- How long do listings remain observable in the collected data?

The dashboard supports exploratory analysis and interactive filtering rather than providing definitive vehicle valuations.

---

## 🏗️ Data Architecture

The Power BI report uses data prepared by the Python data acquisition pipeline.

```text
Online Automotive Marketplace
            │
            ▼
       Python Pipeline
            │
            ▼
       SQLite Database
            │
            ▼
       SQL Analytical Views
            │
            ▼
         CSV Export
            │
            ▼
       Power BI Data Model
            │
            ▼
       Interactive Dashboard
```

The current implementation uses CSV files exported from SQLite as the data source.

This provides a simple local integration between the Python analytical database and Power BI.

---

## 🛠️ Technology Stack

| Technology | Application |
|---|---|
| Microsoft Power BI | Interactive dashboard and reporting |
| Power Query | Data transformation |
| DAX | Measures and calculations |
| SQL | Analytical data preparation |
| SQLite | Source database |
| CSV | Data integration |

---

## 📊 Dashboard Structure

The current report consists of four analytical pages.

### 1. Market Overview

![Market Overview](./images/general-market-overview.png)

Provides a high-level overview of the observed Porsche 911 listing market.

#### Key elements

- KPI cards:
  - Active listings
  - Median asking price
  - Most popular generation
  - Unique listings
  - Newly observed listings per day
  - Observation period
- World map showing countries of origin of listed vehicles.
- Map showing geographical distribution of listings across Poland.
- Box-and-whisker chart comparing asking-price distributions across generations.
- Bar chart showing listing volume by generation.
- Time-series chart tracking active listings.
- Interactive filters.
- Drill-through navigation to generation-level analysis.

#### Analytical questions

- What does the observed Porsche 911 market look like?
- Which generations are most frequently listed?
- How do asking prices differ across generations?
- Where are the listings geographically concentrated?
- How does the number of observed listings change over time?

This page provides the starting point for market exploration.

---

### 2. Generation Drill Through

![Market Overview](./images/generation-drill-through.png)

Provides a detailed analysis of a selected Porsche 911 generation.

The page can be accessed through drill-through navigation from the Market Overview.

#### Key elements

- KPI cards:
  - Median asking price
  - Listing count
  - Median mileage
  - Median model year
- Model year versus median asking price.
- Mileage versus asking price at individual-listing level.
- Engine displacement versus engine power.
- Engine power distribution.
- Engine displacement distribution.
- Gearbox distribution.
- Fuel type distribution.
- Most common engine configurations.
- Drivetrain distribution.
- Body type distribution.

#### Analytical questions

- What characterizes a particular Porsche 911 generation?
- How does asking price vary with model year?
- How does mileage relate to asking price?
- Which technical configurations are most common?
- How do engine specifications differ within a generation?

The purpose of this page is to explore the relationship between vehicle specifications, configuration mix and asking prices.

---

### 3. Price Dynamics

![Market Overview](./images/price-dynamics.png)

Focuses on historical asking-price trends and seller price adjustments.

#### Key elements

- Time-series chart showing median asking prices over time.
- Selectable aggregation:
  - Daily
  - Monthly
  - Quarterly
  - Yearly
- Filters for individual models or the entire Porsche 911 range.
- KPI cards summarizing:
  - Price reductions
  - Price increases
  - Listings with unchanged prices
- Pie chart showing price-change status distribution.
- 100% stacked column chart showing price-change status composition over time.
- Histogram showing the distribution of price adjustments.

#### Analytical questions

- How are asking prices evolving over time?
- How frequently do sellers reduce or increase asking prices?
- What proportion of listings have unchanged prices?
- How large are observed price adjustments?
- Do price adjustment patterns differ across models?

Price-change analysis compares initial and subsequently observed asking prices.

It describes seller behavior and listing price adjustments, not confirmed transaction prices.

---

### 4. Listing Lifecycle

![Market Overview](./images/listing-lifecycle.png)

Analyzes how long listings remain observable in the collected market data.

The current page focuses on inactive listings.

#### Key elements

- KPI cards:
  - Active listing count
  - Median days on market
  - Average days on market
- Distribution chart showing listing duration.
- Comparison of average listing duration across generations.
- Scatter plot comparing asking price and days on market.

#### Analytical questions

- How long do Porsche 911 listings remain observable?
- How does listing duration vary across generations?
- Is there a relationship between asking price and observed listing duration?
- How does the distribution of listing duration look across the collected dataset?

Listing duration is calculated from the period between the first and last observed snapshots.

A listing disappearing from the dataset does not necessarily mean that the vehicle was sold.

---

## 🧠 Analytical Approach

The dashboard is designed around exploratory market analysis.

The report combines:

- Market-level KPIs.
- Market segmentation.
- Asking-price distribution analysis.
- Vehicle specification analysis.
- Historical listing observations.
- Interactive filtering.
- Drill-through navigation.

The analytical questions are defined before designing the visualizations.

This approach helps ensure that each page serves a clear analytical purpose.

---

## 🎓 Skills Demonstrated

### 📊 Power BI & Data Visualization

- Building an interactive Power BI report.
- Designing KPI cards.
- Creating analytical visualizations.
- Market segmentation.
- Interactive filtering.
- Drill-through navigation.
- Time-series analysis.
- Distribution analysis.
- Geographic visualization.

### ⚙️ Power Query

- Data transformation.
- Preparing source data for analytical reporting.
- Integrating CSV datasets into the Power BI model.

### 🧮 DAX & Analytical Modeling

- Creating analytical measures.
- KPI calculations.
- Aggregation of market data.
- Price and listing analysis.
- Time-based analysis.

### 🧠 Business & Analytical Thinking

- Translating business questions into analytical requirements.
- Selecting visualizations based on analytical objectives.
- Understanding market segmentation.
- Interpreting asking-price distributions.
- Exploring relationships between vehicle characteristics and asking prices.
- Distinguishing descriptive analysis from causal interpretation.

---

## ⚠️ MVP Scope & Limitations

The current dashboard is a first working version rather than a finished market valuation product.

Important limitations:

- The analysis is based on collected listings.
- Asking prices are not confirmed transaction prices.
- Dataset coverage depends on the scraper and collection period.
- Historical market analysis becomes more meaningful as additional observations are collected.
- A listing disappearing from the dataset does not automatically mean it was sold.
- Listing duration represents observed time on the platform, not confirmed time to sale.
- Price changes reflect asking-price adjustments, not transaction-price changes.
- Observed relationships between vehicle characteristics and asking prices should not automatically be interpreted as causal.

---

## 🚀 Future Development

Potential future directions include:

- Comparable-vehicle analysis.
- More detailed market segmentation.
- Further historical price analysis.
- Advanced statistical analysis.
- Potential machine learning applications.

These are potential development directions rather than implemented dashboard features.

---

## 📌 Key Takeaway

The Power BI dashboard demonstrates how raw marketplace data can be transformed into an interactive analytical tool.

The report connects market-level analysis with vehicle-level characteristics and historical listing observations.

It provides the first analytical interface for the Porsche 911 Market Intelligence project and establishes a foundation for deeper market research as more historical data becomes available.

