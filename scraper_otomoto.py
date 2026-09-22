import datetime
import random
import time

import requests
from bs4 import BeautifulSoup, Tag
from data_model import SearchAdvertData, AdvertProcessingData, AdvertDetails

import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO
)

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

    def __init__(self, url: str = None, test_mode: bool = False, pages_limit: int = None, adverts_limit: int = None):
        self.seen_advert_ids = set()  # advert ids already scraped within light crawl

        self.first_page_url = url  # first page of search results
        self.test_mode = test_mode
        self.pages_limit = pages_limit
        self.adverts_limit = adverts_limit

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

    @staticmethod
    def get_single_advert_test_path(advert_id):
        return f"html-files/advert_page_{advert_id}.html"

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

    def get_random_pause(self):
        if not self.test_mode:
            pause = random.randint(100, 1000) / 100
        else:
            pause = 0.001

        return pause

    def get_parsed_html(self, url: str) -> BeautifulSoup:
        """
        Downloads raw HTML content from the given URL and returns a BeautifulSoup object.
        While in test_mode, the method reads test.html file instead of downloading it.
        """

        if self.test_mode:
            # print("Testing mode — retrieving data from hard drive")
            # print(f"Path: {url}")
            path = url
            try:
                with open(path, "r", encoding="utf-8") as f:
                    html = f.read()
            except FileNotFoundError:
                # print(f"Błąd: Plik '{path}' nie istnieje!")
                html = None  # lub inna domyślna wartość / obsługa błędu
        else:
            print(f"Downloading {url}")
            # print(f"Time: {datetime.datetime.now()}")
            html = requests.get(url, headers=self.HEADERS).text

        if html:
            soup_doc = BeautifulSoup(html, 'html.parser')
        else:
            soup_doc = None

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
                                price=price, currency=currency, snapshot_date=datetime.date.today(),
                                scraped_at=datetime.datetime.now().replace(microsecond=0)),
                AdvertProcessingData(advert_id=advert_id, city=city, province=province,))


    def scrape_one_page_of_search_results(self, search_results: Tag):
        """Finds all article items in the container and passes each to scrape_single_search_item."""
        articles = search_results.find_all("article", attrs={"data-id": True}, recursive=False)

        for article in articles:
            search_data, processing_data = self.scrape_single_search_item(article)

            if search_data.advert_id in self.seen_advert_ids:
                continue

            self.searched_listings.append(search_data)
            self.listings_processed_info.append(processing_data)

            self.seen_advert_ids.add(search_data.advert_id)


    def scrape_all_pages_of_search_results(self):
        """Iterates through all search pages from 2 to self.last_page_number and scrapes their contents."""
        if not self.last_page_number:
            return

        for page_number in range(2, self.last_page_number + 1):
            pause = self.get_random_pause()
            time.sleep(pause) # Random pause between requests
            # print(f"Pause: {pause}")
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


    def scrape_one_advert_from_url(self, advert_id, data_from_light_crawl: dict) -> AdvertDetails:

        def get_detail(doc, test_id):
            element = doc.find(attrs={"data-testid": test_id})

            if element is None:
                return None

            detail_values = element.find_all("p")

            if not detail_values:
                return None

            return detail_values[-1].get_text(strip=True)

        def get_int_detail(doc, test_id):
            detail_value = get_detail(doc, test_id)

            if detail_value is None:
                return None

            return int(detail_value)

        def convert_to_bool(str_value: str) -> bool | None:
            if str_value is None:
                return None
            if str_value.lower() == "tak":
                return True
            elif str_value.lower() == "nie":
                return False
            else:
                logger.warning("Unknown boolean value from Otomoto: %r", str_value)
                return None

        def get_seller_type(bs_doc):
            if bs_doc.find("svg", attrs={"name": "private-seller"}):
                return "private", None

            if bs_doc.find("svg", attrs={"name": "authorized-dealer"}):
                return "company", "authorized"

            if bs_doc.find("svg", attrs={"name": "dealer"}):
                return "company", "dealer"

            return None, None

        if not self.test_mode:
            url = data_from_light_crawl['url']
        else:
            url = self.get_single_advert_test_path(advert_id)

        soup_doc = self.get_parsed_html(url)  # MAKE A REQUEST!

        if not soup_doc:
            return AdvertDetails(
                advert_id=advert_id,
                engine_size_cm3=None,
                engine_power_hp=None,
                year=None,
                mileage=None,
                mileage_unit=None,
                province=None,
                city=None,
                body_type=None,
                gearbox=None,
                fuel_type=None,
                make=None,
                model=None,
                version=None,
                generation=None,
                drive_type=None,
                color=None,
                no_accident=None,
                country_origin=None,
                service_record=None,
                new_used=None,
                registered_pl=None,
                damaged=None,
                historical_vehicle=None,
                has_registration=None,
                tuning=None,
                original_owner=None,
                long_description=None,
                seller_type=None,
                dealer_type=None,
                first_seen_at=None,
            )

        # Find the section containing all main car details
        main_details = soup_doc.find(
            "div",
            {"data-testid": "main-details-section"}
        )

        # Dictionary to store the extracted car details
        car_details = {}

        # Find each individual detail (e.g. mileage, fuel type, gearbox, etc.)
        for detail in main_details.find_all(
                "div",
                {"data-testid": "detail"}
        ):
            # Each detail contains two <p> elements:
            # the first one contains the value,
            # the second one contains the name of the parameter
            values = detail.find_all("p")

            value = values[0].get_text(strip=True)
            name = values[1].get_text(strip=True)

            # Store the value using the parameter name as the dictionary key
            car_details[name] = value

        # Ensure the right format of the data
        mileage_raw = car_details.get("Przebieg")

        if mileage_raw:
            mileage = int(mileage_raw[:-3].replace(' ', '').strip())
            mileage_unit = mileage_raw[-3:].strip()
        else:
            mileage = None
            mileage_unit = None

        fuel_type = car_details.get("Rodzaj paliwa")
        gearbox = car_details.get("Skrzynia biegów")
        body_type = car_details.get("Typ nadwozia")

        engine_size = car_details.get("Pojemność skokowa")

        if engine_size:
            engine_size = int(engine_size.replace('cm3', '').replace(' ', '').strip())

        power = car_details.get("Moc")

        if power:
            power = int(power.replace('KM', '').replace(' ', '').strip())

        # Section with details underneath
        combined_details_section = soup_doc.find(
            "div",
            attrs={"data-testid": "combined-details-and-equipment-section"}
        )

        if combined_details_section is None:
            raise ValueError("Details section not found")

        make = get_detail(combined_details_section, "make")
        model = get_detail(combined_details_section, "model")
        version = get_detail(combined_details_section, "version")
        year = get_int_detail(combined_details_section, "year")
        generation = get_detail(combined_details_section, "generation")
        drive_type = get_detail(combined_details_section, "transmission")
        color = get_detail(combined_details_section, "color")

        no_accident = get_detail(combined_details_section, "no_accident")
        country_origin = get_detail(combined_details_section, "country_origin")
        service_record = get_detail(combined_details_section, "service_record")
        new_used = get_detail(combined_details_section, "new_used")
        registered_pl = get_detail(combined_details_section, "registered")  # Registered in Poland

        damaged = get_detail(combined_details_section, "damaged")
        historical_vehicle = get_detail(combined_details_section, "historical_vehicle")
        has_registration = get_detail(combined_details_section, "has_registration")
        tuning = get_detail(combined_details_section, "tuning")
        original_owner = get_detail(combined_details_section, "original_owner")

        no_accident = convert_to_bool(no_accident)
        service_record = convert_to_bool(service_record)
        registered_pl = convert_to_bool(registered_pl)
        damaged = convert_to_bool(damaged)
        historical_vehicle = convert_to_bool(historical_vehicle)
        has_registration = convert_to_bool(has_registration)
        tuning = convert_to_bool(tuning)
        original_owner = convert_to_bool(original_owner)

        # Get main description
        description_section = soup_doc.find(
            "div",
            attrs={"data-testid": "content-description-section"}
        )

        if description_section is None:
            description = None
        else:
            description_element = description_section.find(
                "div",
                attrs={"data-testid": "textWrapper"}
            )

            if description_element is None:
                description = None
            else:
                description = description_element.get_text(" ", strip=True)

        # Get seller_type information
        seller_type, dealer_type = get_seller_type(soup_doc)

        return AdvertDetails(advert_id=advert_id, engine_size_cm3=engine_size, engine_power_hp=power, mileage=mileage,
                             mileage_unit=mileage_unit, province=data_from_light_crawl['province'],
                             city=data_from_light_crawl['city'], body_type=body_type, gearbox=gearbox,
                             fuel_type=fuel_type, make=make, model=model, version=version, year=year,
                             generation=generation, drive_type=drive_type, color=color, no_accident=no_accident,
                             country_origin=country_origin, service_record=service_record, new_used=new_used,
                             registered_pl=registered_pl, damaged=damaged, historical_vehicle=historical_vehicle,
                             has_registration=has_registration, tuning=tuning, original_owner=original_owner,
                             long_description=description, seller_type=seller_type, dealer_type=dealer_type,
                             first_seen_at=datetime.date.today())


    def light_crawl(self):
        """Goes over search pages and collects general listings data"""
        self.initialize_search_scraping(self.first_page_url, True)
        self.scrape_all_pages_of_search_results()

    def heavy_crawl(self, new_adverts: dict):
        """Goes over new adverts urls and collects details data"""
        adverts_count = len(new_adverts)

        for advert_number, (advert_id, data) in enumerate(new_adverts.items(), start=1):
            pause = self.get_random_pause()
            time.sleep(pause) # Random pause between requests
            # print(f"Pause: {pause}")
            print(f"Scraping advert {advert_number}/{adverts_count} {advert_id}")

            details = self.scrape_one_advert_from_url(advert_id=advert_id, data_from_light_crawl=data)
            self.advert_details.append(details)

            if self.adverts_limit:
                if advert_number == self.adverts_limit:
                    print("Adverts limit reached")
                    break
