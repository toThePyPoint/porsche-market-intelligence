import datetime

import requests
from bs4 import BeautifulSoup, Tag
from data_model import SearchAdvertData, AdvertDetails


class OtomotoScraper:
    LAST_ITEMS_ID = "ooa-13ptg7a"
    DESCRIPTION_ELEMENT_ID = "e1kj25my0.ooa-nxfgg7"

    def __init__(self, url: str = None, test_mode: bool = False, test_url: str = None):
        self.url = url
        self.test_mode = test_mode
        self.test_url = test_url

        self.last_page_number = None

        self.listings: list[SearchAdvertData] = []

    def get_url_for_given_page_number(self, page_number: int):
        return f"{self.url}?page={page_number}"

    def get_last_page_number(self, soup: BeautifulSoup | Tag):
        """Finds the highest pagination page number and sets self.last_page_number."""
        page_items = soup.find_all("button", class_=self.LAST_ITEMS_ID)

        page_numbers = [
            int(item.get_text(strip=True))
            for item in page_items
            if item.get_text(strip=True).isdigit()
        ]

        self.last_page_number = max(page_numbers) if page_numbers else None

    # @staticmethod
    def get_parsed_html(self, url: str) -> BeautifulSoup:
        """
        Downloads raw HTML content from the given URL and returns a BeautifulSoup object.
        While in test_mode, the method reads test.html file instead of downloading it.
        """

        if self.test_mode:
            print("Testing mode — retrieving data from hard drive")
            with open(self.test_url, "r", encoding="utf-8") as f:
                html = f.read()
        else:
            print(f"Downloading {url}")
            print(f"Time: {datetime.datetime.now()}")
            html = requests.get(url).text

        soup_doc = BeautifulSoup(html, 'html.parser')

        return soup_doc

    @staticmethod
    def get_search_results_from_one_page(soup: BeautifulSoup | Tag):
        """Extracts the main search results container (div[data-testid='search-results']) from the page."""
        search_results = soup.find("div", {"data-testid": "search-results"})
        return search_results

    def scrape_first_search_page_and_get_last_page_num(self):
        """Fetches the first page, scrapes its items, and sets self.last_page_number."""
        soup_doc = self.get_parsed_html(self.url)  # REQUEST!
        self.scrape_one_page_of_search_results(self.get_search_results_from_one_page(soup_doc))
        self.get_last_page_number(soup_doc)

    def scrape_single_search_item(self, article: Tag) -> SearchAdvertData:
        """Extracts required data fields from a single search result article tag."""
        advert_id = article.get("data-id")

        title_element = article.find("h2").find("a")
        title = title_element.get_text(strip=True)
        url = title_element.get("href")

        description_element = article.select_one(f"p.{self.DESCRIPTION_ELEMENT_ID}")
        description = description_element.get_text(strip=True)

        return SearchAdvertData(advert_id=advert_id, title=title, url=url, description=description)


    def scrape_one_page_of_search_results(self, search_results: Tag):
        """Finds all article items in the container and passes each to scrape_single_search_item."""
        articles = search_results.find_all("article", attrs={"data-id": True}, recursive=False)
        for article in articles:
            single_advert_data = self.scrape_single_search_item(article)
            self.listings.append(single_advert_data)

    def scrape_all_pages_of_search_results(self):
        """Iterates through all search pages from 2 to self.last_page_number and scrapes their contents."""
        pass

    def light_crawl(self):
        """Goes over search pages and collects general listings data"""
        self.scrape_first_search_page_and_get_last_page_num()