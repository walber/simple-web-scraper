import json
from abc import ABC
from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest


class Scraper(ABC):
    def __init__(self):
        self._data = None

    @property
    def data(self):
        return self._data

    def scrape(self, page_src):
        pass


class DummyScraper(Scraper):
    def scrape(self, page_src):
        pass


class WebScraper(QApplication):
    def __init__(self, scraper=DummyScraper()):
        super().__init__([])
        self._scraper = scraper
        self.view = QWebEngineView()
        self.view.loadFinished.connect(self._on_load_finished)


    def _print_headers(self, reply):
        hs = (f'{str(h, "utf-8")}: {str(v, "utf-8")}' for h, v in reply.rawHeaderPairs())
        print('\n'.join(hs), end='\n\n')


    def _get_headers(self):
        """Return the request headers dictionary from headers.json"""
        headers = {}       
        try:
            with open('headers.json') as h:
                headers = json.load(h)
        except:
            pass
        finally:
            return headers


    def _callback(self, page_src):
        """Call the scrape function on page source and closes the view"""
        self._scraper.scrape(page_src)
        self.view.close()


    def _on_load_finished(self, successfully):
        """Retrieve the page source a pass it the default callback"""
        if successfully:
            self.view.page().toHtml(self._callback)
        else:
            print('Fail to load:', self.view.url().toString())
            self.view.close()


    def load(self, url):
        """Load the url and sets the headers"""
        request = QWebEngineHttpRequest(QUrl(url))
        headers = self._get_headers()

        for h, v in headers.items():
            request.setHeader(bytearray(str(h), 'utf-8'), bytearray(str(v), 'utf-8'))

        self.view.load(request)

