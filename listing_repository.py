import sqlite3
from pathlib import Path
from dataclasses import astuple, asdict

from data_model import SearchAdvertData, AdvertDetails, ScraperRunsInfo


class ListingRepository:
    SNAPSHOTS_TABLE_NAME = 'listings_snapshots'
    DETAILS_TABLE_NAME = 'listings_details'
    SCRAPER_RUNS_TABLE_NAME = 'scraper_runs_info'

    def __init__(self, db_name: str):
        # self.searched_listings = listings
        self.db_name = db_name

    def set_connection(self):
        """Sets connection to sqlite3 database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        return conn, cursor

    def create_tables(self):
        """Creates tables in database."""
        conn, cursor = self.set_connection()
        try:
            cursor.execute(
                f'''CREATE TABLE IF NOT EXISTS {self.SNAPSHOTS_TABLE_NAME} (
                        advert_id TEXT NOT NULL,
                        snapshot_date DATE NOT NULL,
                        title TEXT NOT NULL,
                        short_description TEXT NOT NULL,
                        price INTEGER NOT NULL,
                        currency TEXT NOT NULL,
                        scraped_at DATETIME NOT NULL,
                        url TEXT NOT NULL,
                        
                        PRIMARY KEY (advert_id, snapshot_date)
                    )
                '''
            )

            cursor.execute(
                f'''CREATE TABLE IF NOT EXISTS {self.DETAILS_TABLE_NAME} (
                        advert_id TEXT PRIMARY KEY,
                        engine_size_cm3 INTEGER,
                        engine_power_hp INTEGER,
                        year INTEGER,
                        mileage INTEGER,
                        mileage_unit TEXT,
                        province TEXT,
                        city TEXT,
                        body_type TEXT,
                        gearbox TEXT,
                        fuel_type TEXT,
                        make TEXT,
                        model TEXT,
                        version TEXT,
                        generation TEXT,
                        drive_type TEXT,
                        color TEXT,
                        no_accident INTEGER,
                        country_origin TEXT,
                        service_record INTEGER,
                        new_used TEXT,
                        registered_pl INTEGER,
                        damaged INTEGER,
                        historical_vehicle INTEGER,
                        has_registration INTEGER,
                        tuning INTEGER,
                        original_owner INTEGER,
                        long_description TEXT,
                        seller_type TEXT,
                        dealer_type TEXT,
                        first_seen_at DATE
                    )
                '''
            )

            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.SCRAPER_RUNS_TABLE_NAME} (
                        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        run_date DATE,
                        run_time TIME,
                        listings_scraped INTEGER,
                        new_listings INTEGER,
                        duplicates INTEGER,
                        id_mismatch INTEGER,
                        missing_mileage INTEGER,
                        missing_version INTEGER,
                        missing_gearbox INTEGER,
                        missing_drive_type INTEGER,
                        missing_fuel_type INTEGER,
                        missing_size INTEGER,
                        missing_power INTEGER,
                        missing_year INTEGER,
                        log_warnings INTEGER
                    )
                """
            )

            conn.commit()
        finally:
            conn.close()

    def create_views(self):
        conn, cursor = self.set_connection()
        conn.executescript(Path("database/views.sql").read_text())

    def insert_listings_to_db(self, listings: list[SearchAdvertData]):
        """Inserts listings into database to table with listings snapshots."""
        conn, cursor = self.set_connection()
        try:
            cursor.executemany(
                f'''INSERT INTO {self.SNAPSHOTS_TABLE_NAME} (
                advert_id, snapshot_date, title, short_description, price, currency, scraped_at, url
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (advert_id, snapshot_date) DO NOTHING
                ''',
                (astuple(item) for item in listings)
            )

            conn.commit()
        finally:
            conn.close()

    def insert_adverts_details_to_db(self, advert_details: list[AdvertDetails]):
        """Inserts listings into database to table with adverts details."""
        conn, cursor = self.set_connection()
        try:
            cursor.executemany(
                f'''INSERT INTO {self.DETAILS_TABLE_NAME} (
                        advert_id,
                        engine_size_cm3,
                        engine_power_hp,
                        year,
                        mileage,
                        mileage_unit,
                        province,
                        city,
                        body_type,
                        gearbox,
                        fuel_type,
                        make,
                        model,
                        version,
                        generation,
                        drive_type, 
                        color,
                        no_accident,    
                        country_origin,
                        service_record,
                        new_used,
                        registered_pl,
                        damaged,
                        historical_vehicle,
                        has_registration,
                        tuning,
                        original_owner,
                        long_description,
                        seller_type,
                        dealer_type,
                        first_seen_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (astuple(item) for item in advert_details)
            )

            conn.commit()
        finally:
            conn.close()

    def insert_scraper_run_info(self, run_info: ScraperRunsInfo):
        """Inserts scraper run details into the database."""
        conn, cursor = self.set_connection()
        try:
            cursor.execute(
                f'''INSERT INTO {self.SCRAPER_RUNS_TABLE_NAME} (
                    run_date, run_time, listings_scraped, new_listings, duplicates, id_mismatch,
                    missing_mileage, missing_version, missing_gearbox, missing_drive_type,
                    missing_fuel_type, missing_size, missing_power, missing_year, log_warnings
                )
                VALUES (
                    :run_date, :run_time, :listings_scraped, :new_listings, :duplicates, :id_mismatch,
                    :missing_mileage, :missing_version, :missing_gearbox, :missing_drive_type,
                    :missing_fuel_type, :missing_size, :missing_power, :missing_year, :log_warnings
                )
                ''',
                asdict(run_info)
            )

            conn.commit()
        finally:
            conn.close()

    def get_all_adverts_from_table_with_details(self) -> list:
        """Gets all adverts ids from table with details."""
        conn, cursor = self.set_connection()
        try:
            cursor.execute(f"SELECT advert_id FROM {self.DETAILS_TABLE_NAME}")
            rows = cursor.fetchall()
            advert_ids = [row[0] for row in rows] # convert to Python list
        finally:
            conn.close()

        return advert_ids