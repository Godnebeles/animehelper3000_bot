import cfscrape
import json

import requests
import re

import urllib
import urllib3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


#title = input("Введите название фильма: ")
#search = "https://yummyanime.club/get-search-list?&word=" + title + "&page=1"
link = " https://yummyanime.club/get-search-list?&word=" + urllib.parse.quote("Домекано")

HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}


def sub_num(parse_str):
    return re.compile('[^0-9]').sub('', parse_str)


def get_html(url, params=None):
    response = Request(url, headers=HEADERS)
    #.content.decode()
    return urlopen(response).read()


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser') #, params=params
    #items = soup.find('table', class_='tbl-switcher').find('tbody').find_all('tr')[0].find_all('td')[5].text
    items = soup.find('div', class_='content-page') #.find_all('div', class_='anime-column')
    ourjJson = json.loads(str(soup))
    print(ourjJson['animes']['data'][0]['name'])

def parse():
    html = get_html(link)
    #if html.status_code == 200:
    get_content(html)
    #else:
        # print(search)
        # print('Error: ' + str(html.status_code))


parse()