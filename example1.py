import sys
from scrapers import AnchorScraper
from web_scraper import WebScraper

def main():
    app = WebScraper(AnchorScraper())
    #url = 'https://www.tercalivre.com.br'
    url = 'https://github.com'
    app.load(url)
    sys.exit(app.exec_())

if __name__ == '__main__': main()
