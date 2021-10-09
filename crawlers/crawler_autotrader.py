
import car_details
import re

visited_pages = set()
urls = list()


def strip(text):
    return '' if text is None else re.sub('\n\r\n', '', text).strip()


def crawl(soup, work_queue, site_context, car_details_file):
    for card_content in soup.find_all('div', {'class': 'product-card-content'}):

        title = f"{strip(card_content.find('h3', {'class': 'product-card-details__title'}).text)} - " \
                f"{strip(card_content.find('p', {'class': 'product-card-details__subtitle'}).text)}"

        sub_title = ''
        if card_content.find('p', {'class': 'product-card-details__attention-grabber'}) is not None:
            sub_title = strip(card_content.find('p', {'class': 'product-card-details__attention-grabber'}).text)

        price = strip(card_content.find('div', {'class': 'product-card-pricing__price'}).text)

        details = []
        for li in card_content.find_all('li', {'class': 'atc-type-picanto--medium'}):
            details.append(strip(li.text))

        seller = strip(card_content.find('h3', {'class': 'product-card-seller-info__name atc-type-picanto'}).text)

        seller_location = ''
        for li in card_content.find_all('li', {'class': 'product-card-seller-info__spec-item atc-type-picanto'}):
            for span in li.find_all('span', {'class': 'product-card-seller-info__spec-item-copy'}):
                seller_location = f'{strip(span.text)} - {strip(span.next_sibling)}'
        # TODO; extract the year and mileage
        year = 0
        for detail in details:
            if re.match('\d{4} \(.* reg\)', detail):
                year = int(detail.split(' ')[0])
            if 'miles' in detail:
                mileage = detail.split(' ')[0]

        car_details.write_to_file(title, sub_title, details, seller, seller_location, price, year, mileage, car_details_file)

    if soup.find('a', {'class': 'pagination--right__active'}) is not None:
        work_queue.put(['autotrader', soup.find('a', {'class': 'pagination--right__active'})['href'], ''])
