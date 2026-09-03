import requests
from bs4 import BeautifulSoup


class OtomotoScraper:
    LAST_ITEMS_ID = "ooa-13ptg7a"

    def __init__(self, url):
        self.url = url
        self.last_page_number = None

    def get_last_page_number(self, doc):
        page_items = doc.find_all(class_=self.LAST_ITEMS_ID)
        if page_items:
            self.last_page_number = page_items[-1].text
        else:
            self.last_page_number = None

    def scrape(self):
        html = requests.get(self.url).text
        soup_doc = BeautifulSoup(html, 'html.parser')
        self.get_last_page_number(soup_doc)
