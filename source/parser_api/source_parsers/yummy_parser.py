import cfscrape
import json

import requests
import re

import urllib
import urllib3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


YUMMY_SEARCH_LINK = " https://yummyanime.club/get-search-list?&word="# + urllib.parse.quote("Домекано")
current_anime_link = "https://yummyanime.club/catalog/item/"


HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}


class YummyParser:
    def __init__(self):
        self.ourjJson = {}


    def sub_num(self, parse_str):
        return re.compile('[^0-9]').sub('', parse_str)


    def get_html(self, url, params=None):
        response = Request(url, headers=HEADERS)
        #.content.decode()
        return urlopen(response).read()


    def get_search_content(self, html):
        soup = BeautifulSoup(html, 'html.parser') #, params=params
        items = soup.find('div', class_='content-page')
        self.ourjJson = json.loads(str(soup))
        return self.ourjJson['animes']['data']


    def get_current_anime_data(self, link):
        soup = BeautifulSoup(self.get_html(link), 'html.parser')
        series_count = len(soup.find('div', class_="block-episodes").find_all('div'))
        return series_count


    def parse(self, title):
        html = self.get_html(YUMMY_SEARCH_LINK + urllib.parse.quote(title))
        #if html.status_code == 200:
        return self.get_search_content(html)
        #else:
            # print(search)
            # print('Error: ' + str(html.status_code))


    def anime_parse(self, alias):
        link = current_anime_link + alias
        return self.get_current_anime_data(link)
    
