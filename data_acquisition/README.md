# Porsche 911 Market Intelligence — Data Acquisition

This module is responsible for collecting, processing, validating and storing Porsche 911 listing data from an online automotive marketplace.

It forms the foundation of the entire Market Intelligence project: the quality and structure of the collected data directly determine the analytical capabilities of the Power BI dashboard.

The implementation focuses on building a repeatable data acquisition process rather than performing a one-time scrape.

---

## 🎯 Objectives

The Python pipeline is designed to:

- Collect Porsche 911 listings from marketplace search results.
- Capture daily listing snapshots to preserve historical observations.
- Retrieve detailed vehicle specifications for new listings.
- Avoid unnecessary requests for listings already processed.
- Validate and normalize collected data.
- Monitor data quality and scraper execution.
- Store structured data in SQLite.
- Prepare analytical datasets for Power BI.

---

## 🏗️ Architecture

The Python implementation follows a modular, class-based architecture.

```text
ListingService
      │
      ├── MarketPlaceScraper
      │       ├── Light Crawl
      │       └── Heavy Crawl
      │
      ├── ListingRepository
      │       ├── SQLite tables
      │       ├── SQL views
      │       └── CSV export
      │
      ├── Data Models
      │       └── Python dataclasses
      │
      └── Exchange Rate API
              └── NBP
```

The architecture separates the responsibilities of data acquisition, data modeling, persistence and orchestration.

### Main components

| Component | Responsibility |
|---|---|
| `scraper.py` | HTML parsing and listing data acquisition |
| `data_model.py` | Structured representation of collected data |
| `listing_repository.py` | SQLite operations, SQL views and CSV export |
| `pipeline.py` | Orchestration of the entire acquisition process |
| `exchange_rates.py` | Retrieval of exchange rates from the NBP API |

---

## 🔎 Data Acquisition

The scraper uses a two-stage approach to collect marketplace data.

### 1. Light Crawl — Search Results

The light crawl processes marketplace search-result pages and collects general listing information.

Collected fields include:

- Advert ID
- Title
- Short description
- Asking price
- Currency
- Listing URL
- City and province
- Snapshot date
- Scraping timestamp

The scraper automatically navigates through search-result pagination.

It also detects duplicate advert IDs within the same crawl.

The light crawl is designed to be relatively efficient because it collects only the information needed to track listing observations and identify new adverts.

### 2. Heavy Crawl — Detailed Vehicle Information

Detailed vehicle attributes are collected only for adverts that are not already present in the detailed database.

This approach reduces unnecessary requests and avoids repeatedly collecting relatively stable vehicle specifications.

The detailed dataset includes:

#### Technical specifications

- Engine displacement
- Engine power
- Model year
- Mileage
- Body type
- Gearbox
- Fuel type
- Drivetrain
- Colour

#### Vehicle identification

- Make
- Model
- Version
- Generation

#### Vehicle history and condition

- Accident history
- Country of origin
- Service record
- Registration status
- Damage indicators
- Historical vehicle indicator
- Tuning indicator
- Original owner indicator

#### Listing information

- Full description
- Seller type
- Dealer type
- First observed date

The scraper also checks whether the advert ID found on the search page matches the ID found on the detailed advert page.

---

## 🧱 Data Modeling

Collected data is represented using Python dataclasses.

This provides structured objects instead of passing loosely organized dictionaries throughout the pipeline.

### `SearchAdvertData`

Represents a listing observation collected during the light crawl.

It contains information such as:

- Advert ID
- Snapshot date
- Title
- Short description
- Price
- Currency
- Scraping timestamp
- URL

### `AdvertProcessingData`

Stores supplementary information used during processing of new adverts, such as geographical location.

### `AdvertDetails`

Represents the detailed vehicle attributes collected during the heavy crawl.

It contains technical specifications, vehicle characteristics, condition indicators and seller information.

### `ScraperRunsInfo`

Represents operational and data quality statistics from a scraper execution.

### `ExchangeRate`

Represents an exchange rate observation stored in the database.

---

## 🗄️ SQLite Database

SQLite is used as a lightweight relational database for local data persistence.

The database separates historical observations, detailed vehicle attributes and operational information.

### `listings_snapshots`

Stores historical observations of listings.

The primary key is:

```sql
PRIMARY KEY (advert_id, snapshot_date)
```

This allows the same advert to be recorded on multiple days while preventing duplicate snapshots for the same advert and date.

The insertion logic uses:

```sql
ON CONFLICT (advert_id, snapshot_date) DO NOTHING
```

This makes repeated insertion of the same daily snapshot idempotent.

### `listings_details`

Stores detailed vehicle attributes.

The primary key is:

```sql
PRIMARY KEY (advert_id)
```

Each advert has one detailed record.

### `scraper_runs_info`

Stores information about scraper executions.

The table includes:

- Run date and time
- Number of listings scraped
- Number of new listings
- Duplicate count
- Advert ID mismatches
- Missing vehicle attributes
- Log warnings

This makes the collection process measurable and provides a historical record of data quality.

### `exchange_rates`

Stores exchange rate observations.

The table uses:

```sql
PRIMARY KEY (rate_date, currency)
```

This allows rates to be stored by date and currency.

---

## 📅 Historical Data Strategy

One of the most important design decisions is storing daily listing snapshots instead of keeping only the latest state of each advert.

For example:

```text
Day 1 → 500,000 PLN
Day 2 → 500,000 PLN
Day 3 → 485,000 PLN
Day 4 → 475,000 PLN
```

This makes it possible to analyze:

- Asking-price changes
- Initial versus current asking prices
- Price reductions and increases
- Listing observation duration
- Historical market supply

A listing disappearing from the source is treated as **no longer observed**, not automatically as a sold vehicle.

---

## 🛡️ Data Quality & Validation

Data quality checks are integrated directly into the acquisition process.

The scraper monitors:

- Duplicate advert IDs.
- Advert ID mismatches between search and detail pages.
- Missing mileage.
- Missing version.
- Missing gearbox.
- Missing drivetrain.
- Missing fuel type.
- Missing engine displacement.
- Missing engine power.
- Missing model year.
- Unexpected boolean values.

### Boolean normalization

Marketplace values such as `"tak"` and `"nie"` are converted into Python boolean values.

Unexpected values are handled separately:

- A warning is logged.
- The value is converted to `None`.
- The warning counter is incremented.

This avoids silently treating unexpected source values as valid data.

### Operational monitoring

Each scraper execution produces a summary containing the number of collected listings and detected data quality issues.

The statistics are stored in SQLite for future monitoring.

This helps distinguish potential market changes from problems in the data collection process.

---

## 🧠 Analytical SQL Layer

SQL views are used to prepare reusable analytical datasets.

One of the key views is:

### `vw_listing_lifecycle`

This view derives listing lifecycle information from historical snapshots, including:

- First observed date
- Last observed date
- Days on market / observed duration
- Number of snapshots
- Minimum asking price
- Maximum asking price
- Initial asking price
- Current asking price
- Price change

The analytical logic is implemented in SQL rather than being duplicated across Power BI measures.

This creates a separation between data acquisition, storage, analytical logic and visualization.

---

## 💱 Exchange Rate Integration — NBP API

The project retrieves exchange rates using the National Bank of Poland (NBP) API.

The implementation uses:

- Python `requests`
- NBP exchange rate API
- JSON response parsing

The current implementation retrieves the applicable average exchange rate for a specified currency using the API endpoint:

```text
https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/
```

The retrieved rate is stored in the `exchange_rates` table together with the date and currency.

This provides a structured way to persist exchange rate observations alongside the listing data.

**Current implementation:** The pipeline requests the EUR exchange rate and stores the result in SQLite.

---

## 🔄 End-to-End Pipeline

The main workflow is orchestrated by `ListingService`.

```text
1. Light crawl
        ↓
2. Initialize database tables and SQL views
        ↓
3. Insert daily listing snapshots
        ↓
4. Identify adverts not present in detailed database
        ↓
5. Heavy crawl for new adverts
        ↓
6. Insert detailed vehicle data
        ↓
7. Record scraper execution statistics
        ↓
8. Retrieve and store exchange rate
        ↓
9. Export database tables and views to CSV
        ↓
10. Print execution summary
```

The process is designed to be repeatable, with historical observations accumulated over time.

---

## 📤 Data Export

The repository provides a CSV export mechanism using Pandas.

The export process:

- Reads SQLite tables and views.
- Converts each database object into a Pandas DataFrame.
- Exports each object to a separate CSV file.
- Uses UTF-8 with BOM encoding (`utf-8-sig`).

The resulting CSV files are used as the data source for Power BI.

The current SQLite → CSV → Power BI integration is intentionally simple and local.

---

## 🛠️ Technology Stack

| Technology | Application |
|---|---|
| Python | Pipeline implementation |
| Requests | HTTP requests and API integration |
| BeautifulSoup | HTML parsing |
| Python dataclasses | Structured data models |
| SQLite | Relational data persistence |
| `sqlite3` | Database operations |
| SQL | Analytical views and data processing |
| Pandas | Data export |
| Logging | Monitoring and warnings |
| Git / GitHub | Version control |

---

## 🎓 Skills Developed

### 🐍 Python Programming

- Object-oriented programming.
- Class-based application architecture.
- Modular code organization.
- Type hints and dataclasses.
- Working with external libraries.
- File handling and path management.
- Exception handling.
- Logging and operational monitoring.

### 🌐 Web Scraping & Data Acquisition

- HTTP requests using Requests.
- HTML parsing with BeautifulSoup.
- CSS selectors and HTML attributes.
- Pagination handling.
- Two-stage scraping architecture.
- Extracting structured information from semi-structured HTML.
- Handling missing and unexpected source data.

### 🗄️ Database & SQL

- Relational database design.
- Primary keys and composite keys.
- Data persistence.
- Idempotent insert operations.
- SQL analytical views.
- Separating historical observations from entity attributes.
- Database repository pattern.

### 🔄 Data Engineering Fundamentals

- ETL pipeline orchestration.
- Data modeling.
- Data normalization.
- Data validation.
- Data quality monitoring.
- Operational logging.
- Historical data collection.
- Data export and integration with BI tools.

### 🔌 API Integration

- HTTP API requests.
- JSON response parsing.
- External data integration.
- Persisting exchange rate observations.

---

## 📌 Current Scope & Limitations

- Data is collected from an online marketplace.
- The scraper depends on the marketplace's HTML structure.
- Historical data coverage increases over time.
- The detailed database stores one record per advert.
- Listing disappearance does not confirm a sale.
- The current database and CSV integration are local.
- The pipeline is designed as an educational and portfolio project.

---

## 🚀 Future Development

Potential directions include:

- Extending historical observations.
- Improving data quality monitoring.
- More advanced analytical datasets.
- Comparable-vehicle analysis.
- Further development of the Power BI dashboard.

These are development ideas rather than implemented capabilities.

---

## 📌 Key Takeaway

The Data Acquisition module demonstrates how to build a structured data collection process that goes beyond scraping individual web pages.

It combines automated acquisition, data modeling, persistence, validation, monitoring and analytical preparation into a reusable Python pipeline.

