# Simple PyQt5 Web Scraper

PyQt web scrapers can scrape both static **and dynamic** web pages. To run this web scraper you must perform the following steps to setup your environment.

### Install **pipenv**, _"a dependency manager for Python projects."_
```
pip install --user pipenv
```
### Clone this repository
```
git clone https://github.com/walber/simple-web-scraper.git
```
### Launch a subshell and activate the virtual environment
```
pipenv shell
```
# Into the code
## _headers.json_
Avoid being blocked by some servers by using the default headers. Here you can set the request headers. Notice that I'm using the IPhone (mobile view) *user-agent*, which usually has fewer visual elements (loads faster) than desktop view.
```json
{
  "accept": "webp,image/apng,image/*,*/*;q=0.8",
  "accept-encoding": "gzip, deflate, br",
  "accept-language": "en-US,en;q=0.9",
  "connection": "keep-alive",
  "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
}
```
## _web_scraper.py_
This file contains the core of the application.
```python
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
        """Call the scrape function on page source and close the view"""
        self._scraper.scrape(page_src)
        self.view.close()


    def _on_load_finished(self, successfully):
        """Retrieve the page source and pass it to the default callback"""
        if successfully:
            self.view.page().toHtml(self._callback)
        else:
            print('Fail to load:', self.view.url().toString())
            self.view.close()


    def load(self, url):
        """Load the url and sets the request headers"""
        request = QWebEngineHttpRequest(QUrl(url))
        headers = self._get_headers()

        for h, v in headers.items():
            request.setHeader(bytearray(str(h), 'utf-8'), bytearray(str(v), 'utf-8'))

        self.view.load(request)

```
## _scrapers.py_
The following classes are implementation of the abstract *Scraper* class from _web_scraper.py_. In this example, I used **BeautifulSoup** library to perform scrape functions. 
```python
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

```
## _example1.py_
The following example will print all the links available on _https:/github.com_
```python
import sys
from scrapers import AnchorScraper
from web_scraper import WebScraper

def main():
    app = WebScraper(AnchorScraper())
    url = 'https://github.com'
    app.load(url)
    sys.exit(app.exec_())

if __name__ == '__main__': main()
```
