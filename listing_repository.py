import sqlite3
from dataclasses import astuple

from data_model import SearchAdvertData, AdvertDetails


class ListingRepository:
    SNAPSHOTS_TABLE_NAME = 'listings_snapshots'
    DETAILS_TABLE_NAME = 'listings_details'

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
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        advert_id TEXT NOT NULL,
                        title TEXT NOT NULL,
                        short_description TEXT NOT NULL,
                        price INTEGER NOT NULL,
                        currency TEXT NOT NULL,
                        scraped_at DATETIME NOT NULL,
                        url TEXT NOT NULL
                    )
                '''
            )

            # TODO: reconsider NOT NULL constraint
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
                        no_accident TEXT,
                        country_origin TEXT,
                        service_record TEXT,
                        new_used TEXT,
                        registered_pl TEXT,
                        damaged TEXT,
                        historical_vehicle TEXT,
                        has_registration TEXT,
                        registration_number TEXT,
                        tuning TEXT,
                        original_owner TEXT,
                        long_description TEXT,
                        first_seen_at DATE
                    )
                '''
            )

            conn.commit()
        finally:
            conn.close()

    def insert_listings_to_db(self, listings: list[SearchAdvertData]):
        """Inserts listings into database to table with listings snapshots."""
        conn, cursor = self.set_connection()
        try:
            cursor.executemany(
                f'''INSERT INTO {self.SNAPSHOTS_TABLE_NAME} (
                advert_id, title, short_description, price, currency, scraped_at, url
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
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
                        registration_number,
                        tuning,
                        original_owner,
                        long_description,
                        first_seen_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (astuple(item) for item in advert_details)
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