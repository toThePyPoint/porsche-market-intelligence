import datetime
import random
import time

import requests
from bs4 import BeautifulSoup, Tag
from data_model import SearchAdvertData, AdvertProcessingData, AdvertDetails


class OtomotoScraper:
    LAST_ITEMS_ID = "ooa-13ptg7a"
    SHORT_DESCRIPTION_ELEMENT_ID = "e1kj25my0.ooa-nxfgg7"
    LOCATION_ID = "ooa-1nqstmz"

    HEADERS = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "pl,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"
    }

    def __init__(self, url: str = None, test_mode: bool = False, pages_limit: int = None):
        self.first_page_url = url  # first page of search results
        self.test_mode = test_mode
        self.pages_limit = pages_limit

        self.last_page_number = None
        self.searched_listings: list[SearchAdvertData] = []  # general information retrieved within light crawl
        self.listings_processed_info: list[AdvertProcessingData] = [] # details retrieved within light crawl
        self.advert_details: list[AdvertDetails] = [] # details retrieved within heavy crawl

        self.set_test_mode()

    def set_test_mode(self):
        """Sets class into testing mode. Testing mode gets HTML files from hard drive."""
        if self.test_mode:
            self.first_page_url = "html-files/preview.html"
            self.last_page_number = 3

    def get_url_for_given_page_number(self, page_number: int):
        return f"{self.first_page_url}?page={page_number}"

    def get_test_path_for_given_page_number(self, page_number: int):
        return self.first_page_url.replace(".html", str(f"_page{page_number}.html"))


    def get_last_page_number(self, soup: BeautifulSoup | Tag):
        """Finds the highest pagination page number and sets self.last_page_number."""
        page_items = soup.find_all("button", class_=self.LAST_ITEMS_ID)

        page_numbers = [
            int(item.get_text(strip=True))
            for item in page_items
            if item.get_text(strip=True).isdigit()
        ]

        if not self.test_mode:
            self.last_page_number = max(page_numbers) if page_numbers else None


    def get_parsed_html(self, url: str) -> BeautifulSoup:
        """
        Downloads raw HTML content from the given URL and returns a BeautifulSoup object.
        While in test_mode, the method reads test.html file instead of downloading it.
        """

        if self.test_mode:
            print("Testing mode — retrieving data from hard drive")
            print(f"Path: {url}")
            with open(url, "r", encoding="utf-8") as f:
                html = f.read()
        else:
            print(f"Downloading {url}")
            print(f"Time: {datetime.datetime.now()}")
            html = requests.get(url, headers=self.HEADERS).text

        soup_doc = BeautifulSoup(html, 'html.parser')

        return soup_doc


    def initialize_search_scraping(self, url, fetch_last_page_num: bool = False) -> None:
        """Fetches and scrapes a single search results page.

        Args:
            url: The target page URL to fetch and process.
            fetch_last_page_num: If True, extracts the total page count
                from the response and updates self.last_page_number.

        Side Effects:
            Appends parsed items to the internal storage.
            Optionally updates self.last_page_number.
        """
        soup_doc = self.get_parsed_html(url)  # MAKE A REQUEST!

        # Extracts the main search results container (div[data-testid='search-results']) from the page.
        search_results = soup_doc.find("div", {"data-testid": "search-results"})
        self.scrape_one_page_of_search_results(search_results)

        if fetch_last_page_num:
            self.get_last_page_number(soup_doc)


    def scrape_single_search_item(self, article: Tag) -> tuple[SearchAdvertData, AdvertProcessingData]:
        """Extracts required data fields from a single search result article tag."""
        advert_id = article.get("data-id")

        title_element = article.find("h2").find("a")
        title = title_element.get_text(strip=True)
        url = title_element.get("href")

        short_description_element = article.select_one(f"p.{self.SHORT_DESCRIPTION_ELEMENT_ID}")
        description = short_description_element.get_text(strip=True)

        price_element = article.find("h3")
        price = int(price_element.get_text(strip=True).replace(" ", ""))

        currency_element = price_element.find_next("p", translate="no")
        currency = currency_element.get_text(strip=True)

        location_element = article.find("p", class_=self.LOCATION_ID)
        location = location_element.get_text(strip=True)
        city, province = location.replace(")", "").split(" (")

        return (SearchAdvertData(advert_id=advert_id, title=title, url=url, short_description=description,
                                price=price, currency=currency, scraped_at=datetime.datetime.now()),
                AdvertProcessingData(advert_id=advert_id, city=city, province=province,))


    def scrape_one_page_of_search_results(self, search_results: Tag):
        """Finds all article items in the container and passes each to scrape_single_search_item."""
        articles = search_results.find_all("article", attrs={"data-id": True}, recursive=False)
        for article in articles:
            search_data, processing_data = self.scrape_single_search_item(article)
            self.searched_listings.append(search_data)
            self.listings_processed_info.append(processing_data)


    def scrape_all_pages_of_search_results(self):
        """Iterates through all search pages from 2 to self.last_page_number and scrapes their contents."""
        if not self.last_page_number:
            return

        for page_number in range(2, self.last_page_number + 1):
            if not self.test_mode:
                pause = random.randint(100, 1000) / 100
            else:
                pause = 0.1

            time.sleep(pause) # Random pause between requests
            print(f"Pause: {pause}")
            print("Scraping page " + str(page_number))

            if self.test_mode:
                page_url = self.get_test_path_for_given_page_number(page_number)
            else:
                page_url = self.get_url_for_given_page_number(page_number)
            self.initialize_search_scraping(page_url)

            if self.pages_limit:
                if page_number == self.pages_limit:
                    print("Pages limit reached")
                    break


    def light_crawl(self):
        """Goes over search pages and collects general listings data"""
        self.initialize_search_scraping(self.first_page_url, True)
        self.scrape_all_pages_of_search_results()