from web_scraper import Scraper
from bs4 import BeautifulSoup as bs

class AnchorScraper(Scraper):
    def scrape(self, page_src):
        """Return the list of href attribute from all anchor elements on the page"""
        soup = bs(page_src, 'html.parser')
        self._data = list(map(lambda a : a.get('href'), soup.find_all('a')))
        print(self._data)


class TextScraper(Scraper):
    def scrape(self, page_src):
        """Return the page text"""
        soup = bs(page_src, 'html.parser')
        self._data = soup.text.split()

