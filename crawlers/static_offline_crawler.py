
from bs4 import BeautifulSoup

import bs4
import logging
import car_details
import re
# import urllib.parse as urlparse

visited_pages = set()
urls = list()


def strip(text):
    return re.sub(r'\s+', '', text).strip()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(lineno)d %(funcName)s %(message)s',
)


def start_static_crawler(log):
    logging.info(f"start_static_crawler for [{log}]")
    html = open(log, 'r+', encoding='utf-8').read()
    soup = BeautifulSoup(html, features='html.parser')
    crawl(soup)


def strip(text):
    return '' if text is None else re.sub('\n\r\n', '', text).strip()


def crawl(soup):
    for card_content in soup.find_all('div', {'class': 'product-card-content'}):

        price = strip(card_content.find('div', {'class': 'product-card-pricing__price'}).text)
        title = strip(card_content.find('p', {'class': 'product-card-details__subtitle'}).text)
        sub_title = strip(card_content.find('p', {'class': 'product-card-details__attention-grabber'}).text)

        details = []
        for li in card_content.find_all('li', {'class': 'atc-type-picanto--medium'}):
            details.append(strip(li.text))

        seller = strip(card_content.find('h3', {'class': 'product-card-seller-info__name atc-type-picanto'}).text)

        seller_location = ''
        for li in card_content.find_all('li', {'class': 'product-card-seller-info__spec-item atc-type-picanto'}):
            for span in li.find_all('span', {'class': 'product-card-seller-info__spec-item-copy'}):
                seller_location = f'{strip(span.text)} - {strip(span.next_sibling)}'


if __name__ == "__main__":
    start_static_crawler('../log/log.html')
