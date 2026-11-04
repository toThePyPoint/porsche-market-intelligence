# Porsche 911 Market Intelligence

Porsche 911 Market Intelligence is an educational data analytics project that builds a historical database of Porsche 911 listings from online marketplace and uses it to analyze the current state, segmentation, pricing and dynamics of the market.

The project combines **Python, web scraping, data modeling, SQLite, SQL and Power BI** into one end-to-end analytical pipeline.

The goal is not only to build a scraper or a dashboard, but to demonstrate how a technical manager can design a small data product: from automated data acquisition and data quality controls, through structured storage and analytical views, to business-oriented reporting.

> **Project status:** The Python data pipeline and analytical database are implemented. The first Power BI dashboard MVP is complete. The project will continue to evolve as more historical observations are collected and additional analyses are developed.

---

## Project objective

The project is designed to answer questions such as:

- What does the Porsche 911 market currently look like?
- How is the market segmented by model, generation, body type, drivetrain, engine and other characteristics?
- What are the typical asking prices for different segments?
- How do prices and supply change over time?
- How long do listings remain in the observed market?
- How frequently do sellers change asking prices?
- How do mileage, specification and other vehicle characteristics relate to asking prices?

The analytical questions are intentionally defined before building the Power BI report. This keeps the dashboard focused on decision-relevant insights rather than simply displaying available data.

---

## Solution architecture

The current architecture follows an end-to-end data pipeline:

```text
Online-marketplace
   │
   ▼
Python scraper
   │
   ├── Light crawl
   │      └── search result data
   │
   └── Heavy crawl
          └── detailed vehicle data
   │
   ▼
Data validation & normalization
   │
   ▼
SQLite database
   │
   ├── listings_snapshots
   ├── listings_details
   └── scraper_runs_info
   │
   ▼
SQL analytical views
   │
   ▼
CSV export
   │
   ▼
Power BI
   │
   ▼
Market Intelligence dashboard
```

The SQLite → CSV → Power BI step is currently used as a simple local bridge between the analytical database and Power BI. A cloud database solution such as BigQuery may be considered later, but it is intentionally outside the current scope.

---

## Data acquisition

### Source

The project uses automotive marketplace as the source of Porsche 911 listing data.

The scraper performs two levels of data collection:

### 1. Light crawl

The light crawl goes through the search-result pages and collects information that is useful for tracking listing snapshots:

- `advert_id`
- title
- short description
- price
- currency
- URL
- location
- snapshot date
- scraping timestamp

The scraper also detects duplicate advert IDs during the crawl.

### 2. Heavy crawl

Detailed vehicle information is collected only for adverts that are not already present in the detailed database.

The detailed dataset includes, among other fields:

- engine displacement
- engine power
- year
- mileage
- body type
- gearbox
- fuel type
- make
- model
- version
- generation
- drivetrain
- colour
- accident history
- country of origin
- service record
- registration status
- damage indicators
- historical vehicle indicator
- tuning indicator
- original owner indicator
- description
- seller type
- dealer type
- first seen date

This two-stage approach reduces unnecessary requests and separates **market snapshots** from relatively stable **vehicle attributes**.

---

## Data model

The project currently uses three main database tables.

### `listings_snapshots`

Stores the state of a listing observed on a particular day.

The primary key is:

```text
(advert_id, snapshot_date)
```

This allows the same advert to be recorded repeatedly over time while preventing duplicate snapshots for the same advert and day.

The table contains fields such as:

- `advert_id`
- `snapshot_date`
- `title`
- `short_description`
- `price`
- `currency`
- `scraped_at`
- `url`

### `listings_details`

Stores detailed attributes of a vehicle.

`advert_id` is the primary key because the detailed record represents the vehicle/listing entity rather than an individual daily observation.

This table contains structured vehicle information collected during the heavy crawl.

### `scraper_runs_info`

Stores information about every scraper execution.

The table records operational and data-quality indicators such as:

- number of listings scraped
- number of new listings
- duplicates
- advert ID mismatches
- missing mileage
- missing version
- missing gearbox
- missing drivetrain
- missing fuel type
- missing engine size
- missing engine power
- missing year
- log warnings

This makes the data acquisition process itself measurable and auditable.

---

## Data quality

Data quality is treated as part of the pipeline rather than as an afterthought.

The scraper performs checks including:

- duplicate advert detection
- consistency check between the advert ID found on the search page and the advert ID found on the detailed page
- detection of missing vehicle attributes
- conversion and validation of boolean values
- logging of unexpected values
- recording of scraper-run quality statistics

The scraper maintains counters for missing attributes and warnings, and these results are persisted in the database.

This provides visibility into whether changes in the analytical data may be caused by actual market behavior or by problems in the collection process.

---

## Historical market data

A key design decision is to store **daily listing snapshots** instead of keeping only the latest state of each advert.

This makes it possible to reconstruct how the observed market changes over time.

For example, the same advert can have:

```text
Day 1 → 500,000 PLN
Day 2 → 500,000 PLN
Day 3 → 485,000 PLN
Day 4 → 475,000 PLN
```

This allows the analytical layer to identify price changes and listing lifecycle patterns.

A listing disappearing from the source is treated as **no longer observed**, not automatically as a sold vehicle. The data therefore does not claim that an advert was sold.

---

## Analytical SQL layer

The database contains SQL views that prepare the raw tables for analysis.

One of the key analytical views is:

### `vw_listing_lifecycle`

This view derives listing-level lifecycle information from the historical snapshots, including concepts such as:

- first observed date
- last observed date
- duration of observation
- number of snapshots
- minimum price
- maximum price
- initial price
- current price
- price change

The purpose of the analytical layer is to move reusable business logic out of the Power BI report and into SQL where appropriate.

This creates a clearer separation between:

```text
Data collection
      ↓
Data storage
      ↓
Analytical logic
      ↓
Visualization
```

---

## Power BI — analytical layer (MVP)

The first Power BI dashboard MVP has been completed. It is the first analytical interface built on top of the data collected by the Python pipeline.

The dashboard is intended to help explore the Porsche 911 listing market from several perspectives:

- **Market overview:** a high-level view of the listings currently represented in the dataset.
- **Price analysis:** exploration of asking-price levels and their distribution.
- **Market segmentation:** comparison of Porsche 911 listings across generations, models/versions and vehicle characteristics.
- **Vehicle characteristics:** analysis of how model year and mileage relate to asking prices.
- **Interactive exploration:** filtering the report to investigate specific subsets of listings rather than relying only on static totals.

The MVP focuses on establishing a useful analytical baseline from the available listing data. It is intentionally not presented as a finished market valuation tool or as a definitive estimate of transaction prices.

### Analytical questions

The first version of the report is designed to support questions such as:

- What does the observed Porsche 911 listing market look like?
- How are asking prices distributed?
- How do asking prices differ across generations and versions?
- How does model year relate to asking price?
- How does mileage relate to asking price?
- How does the market change when the user filters by vehicle characteristics?

These are exploratory questions. Asking prices are not the same as final transaction prices, and relationships shown in the dashboard should not automatically be interpreted as causal.

### MVP scope and limitations

The current dashboard is a **first working version**, not the final Market Intelligence product.

- The analysis is based on collected listings.
- The dataset represents advertised prices, not confirmed sale prices.
- The available sample and its coverage depend on the scraper and collection period.
- Historical snapshots are being accumulated over time; analyses of long-term market dynamics will become more meaningful as the history grows.
- A listing that is no longer observed should not automatically be interpreted as a sold vehicle.

The current MVP provides the foundation for extending the report with historical supply trends, price changes, listing lifecycle analysis and more advanced comparisons.

### Planned Power BI enhancements

Potential next iterations include:

- market supply and listing trends over time
- newly observed and no-longer-observed listings
- price reductions and listing price history
- listing lifecycle and observed time on market
- comparisons between similar vehicles
- more advanced analysis of configuration premiums, such as transmission or drivetrain
- a dedicated comparable-listing analysis

These are future enhancements, not features claimed to be implemented in the current MVP.

---

## Technology stack

| Area | Technology |
|---|---|
| Data acquisition | Python |
| Web scraping | Requests, BeautifulSoup |
| Data structures | Python dataclasses |
| Database | SQLite |
| Database access | Python `sqlite3` |
| Analytical layer | SQL views |
| Data export | Pandas / CSV |
| BI & visualization | Microsoft Power BI |
| Power BI transformation | Power Query |
| Power BI calculations | DAX |
| Version control | Git / GitHub |

---

## Project structure

The core Python layer is organized around separate responsibilities:

```text
scraper.py
    └── OnlineMarketplaceScraper
        └── data acquisition and parsing

data_model.py
    └── dataclasses
        ├── SearchAdvertData
        ├── AdvertProcessingData
        ├── AdvertDetails
        └── ScraperRunsInfo

listing_repository.py
    └── ListingRepository
        └── database operations

pipeline.py
    └── ListingService
        └── end-to-end orchestration
```

The pipeline orchestrates the process:

```text
light crawl
    ↓
database initialization
    ↓
snapshot insertion
    ↓
identification of new adverts
    ↓
heavy crawl
    ↓
details insertion
    ↓
scraper-run quality logging
    ↓
SQL views
    ↓
CSV export
```

This separation keeps scraping, data modeling, persistence and orchestration independent from each other.

---

## Why this project?

This is an **educational and portfolio project** created to develop and demonstrate practical skills at the intersection of:

- data analytics
- Python programming
- SQL
- business intelligence
- automation
- data engineering concepts
- analytical thinking

The project is deliberately built as a complete system rather than as an isolated notebook or visualization exercise.

From a professional perspective, it demonstrates the ability to connect a business question with a technical implementation:

```text
Business question
      ↓
Data acquisition
      ↓
Data model
      ↓
Data quality
      ↓
Analytical logic
      ↓
BI model
      ↓
Dashboard
      ↓
Business insight
```

The Porsche 911 market is used as a practical domain for developing these capabilities.

---

## Current status

- [x] Light crawl
- [x] Heavy crawl
- [x] Data parsing and normalization
- [x] Duplicate detection
- [x] Advert ID consistency check
- [x] Data-quality monitoring
- [x] SQLite database
- [x] Historical listing snapshots
- [x] Listing details table
- [x] Scraper run logging
- [x] SQL analytical views
- [x] SQLite → CSV export for Power BI
- [x] Power BI data model
- [x] Power BI dashboard
- [x] Market segmentation analysis
- [x] Price and market dynamics analysis
- [ ] Comparable listing analysis
- [ ] Final documentation and portfolio presentation

---

## Project roadmap

The project is being developed incrementally:

### Phase 1 — Data acquisition
Build a reliable and repeatable scraper.

### Phase 2 — Data storage
Design a database capable of storing both current listing attributes and historical observations.

### Phase 3 — Data quality
Introduce validation, logging and scraper-run monitoring.

### Phase 4 — Analytical layer
Create SQL views that transform operational data into reusable analytical datasets.

### Phase 5 — Business intelligence
Build the Power BI data model and dashboard around defined market questions.

### Phase 6 — Advanced analytics
Extend the project with comparable-vehicle analysis and potentially more advanced statistical or machine-learning approaches.

---

## Current milestone

The project has reached its first end-to-end milestone: automated data collection, persistence of historical observations, an SQL analytical layer and a working Power BI dashboard MVP. The next iteration will focus on improving the analytical depth rather than rebuilding the data acquisition foundation.

## Project philosophy

The project follows a simple principle:

> **Good analytics starts with good questions and a reliable data pipeline.**

The dashboard is therefore the final layer of the system, not the starting point.

The objective is to create a small but complete **Market Intelligence platform** that continuously collects market data and turns it into structured information that can be explored, compared and analyzed over time.
