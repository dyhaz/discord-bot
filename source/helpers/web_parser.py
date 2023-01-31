from urllib.request import urlopen
from bs4 import BeautifulSoup


class WebParser:
    def __init__(self, url=''):
        self.url = url

    def get_price(self):
        response = urlopen(self.url).read()


