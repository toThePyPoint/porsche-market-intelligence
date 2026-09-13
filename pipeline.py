from data_model import SearchAdvertData
from listing_repository import ListingRepository
from scraper_otomoto import OtomotoScraper


class ListingService:
    DB_NAME = 'test_db.db'

    def __init__(self, test_mode = False):
        self.repo = None
        self.scraper = OtomotoScraper(test_mode=test_mode)

    def identify_new_adverts(self):
        """Identifies new adverts for which heavy crawl needs to be done."""
        pass

    def process(self):
        """Main pipeline of gathering adverts."""
        self.scraper.light_crawl()

        self.repo = ListingRepository(self.scraper.searched_listings, self.DB_NAME)
        self.repo.create_tables()
        self.repo.insert_listings_to_db()

        # TODO: Identify new adverts

        # TODO: Run Heavy crawling from scraper