from data_model import SearchAdvertData, AdvertProcessingData
from listing_repository import ListingRepository
from scraper_otomoto import OtomotoScraper


class ListingService:
    def __init__(self, url: str = None, test_mode: bool = False, pages_limit: int = None, adverts_limit:int = None,
                 db_name: str = "test_db.db"):
        self.db_name = db_name
        self.repo = None
        self.scraper = OtomotoScraper(url=url, test_mode=test_mode, pages_limit=pages_limit, adverts_limit=adverts_limit)

    @staticmethod
    def identify_new_adverts(listings_processed_info: list[AdvertProcessingData],
                             searched_listings: list[SearchAdvertData],
                             adverts_in_db) -> dict:
        """
        Identifies new adverts for which heavy crawl needs to be done.
        Returns dictionary {advert_id: {'url': url, 'province': province, 'city': city}}
        """
        search_advert_list = [advert for advert in searched_listings if advert.advert_id not in adverts_in_db]
        advert_processing_list = [advert for advert in listings_processed_info if advert.advert_id not in adverts_in_db]

        details_map = {item.advert_id: item for item in advert_processing_list}

        result = {
            search_item.advert_id: {
                'url': search_item.url,
                'province': details_map[search_item.advert_id].province,
                'city': details_map[search_item.advert_id].city,
                }
            for search_item in search_advert_list
            if search_item.advert_id in details_map
        }

        return result

    def process(self):
        """Main pipeline of gathering adverts."""
        self.scraper.light_crawl()

        self.repo = ListingRepository(self.db_name)
        self.repo.create_tables()

        self.repo.insert_listings_to_db(self.scraper.searched_listings)

        # Identify new adverts
        adverts_in_db = self.repo.get_all_adverts_from_table_with_details()

        new_adverts = self.identify_new_adverts(self.scraper.listings_processed_info,
                                                self.scraper.searched_listings,
                                                adverts_in_db
                                                )

        self.scraper.heavy_crawl(new_adverts)
        self.repo.insert_adverts_details_to_db(self.scraper.advert_details)

        print(f"Total adverts scraped: {len(self.scraper.searched_listings)}")
        print(f"Found {len(new_adverts)} new adverts.")
        print(f"Id missmatch detected: {self.scraper.id_missmatch_count}")
        print(f"Duplicates found during light crawl: {self.scraper.adverts_duplicates_count}")
