import sqlite3

from data_model import SearchAdvertData


class ListingRepository:
    def __init__(self, listings: list[SearchAdvertData], db_name: str):
        self.listings = listings
        self.db_name = db_name

    def set_connection(self):
        """Sets connection to sqlite3 database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        return conn, cursor

    def create_tables(self):
        """Creates tables in database."""
        conn, cursor = self.set_connection()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS listings_snapshots (
                    advert_id TEXT UNIQUE NOT NULL,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    currency TEXT NOT NULL,
                    province TEXT NOT NULL,
                    city TEXT NOT NULL,
                    scraped_at DATETIME NOT NULL
                )
            '''
        )

        conn.commit()
        conn.close()