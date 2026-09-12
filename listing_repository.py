import sqlite3
from dataclasses import astuple

from data_model import SearchAdvertData


class ListingRepository:
    SNAPSHOTS_TABLE_NAME = 'listings_snapshots'
    DETAILS_TABLE_NAME = 'listings_details'

    def __init__(self, listings: list[SearchAdvertData], db_name: str):
        self.searched_listings = listings
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

            cursor.execute(
                f'''CREATE TABLE IF NOT EXISTS {self.DETAILS_TABLE_NAME} (
                        advert_id TEXT PRIMARY KEY,
                        city TEXT NOT NULL,
                        province TEXT NOT NULL
                    )
                '''
            )

            conn.commit()
        finally:
            conn.close()

    def insert_listings_to_db(self):
        conn, cursor = self.set_connection()
        try:
            cursor.executemany(
                f'''INSERT INTO {self.SNAPSHOTS_TABLE_NAME} (
                advert_id, title, short_description, price, currency, scraped_at, url
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (astuple(item) for item in self.searched_listings)
            )

            conn.commit()
        finally:
            conn.close()