
import configparser
import retry
import crawler_autotrader
import logging
import queue
from bs4 import BeautifulSoup

from datetime import datetime
from shutil import copyfile

work_queue = queue.Queue()
max_pages = 2

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(threadName)s] %(funcName)s:%(lineno)d %(message)s',
)


def process_root(root):
    logging.info('reading urls from ' + root)
    config = configparser.RawConfigParser()
    config.read(root)

    for section in config.sections():
        logging.info('adding link for [' + section + '] to work_queue')
        work_queue.put([section, config[section]['root'], config[section]['url']])


def process_work_queue(json):
    html_file = open('log/log_' + datetime.now().strftime("%y-%m-%d_%H.%M") + '.html', 'w+', encoding='utf-8')
    while not work_queue.empty():
        work_item = work_queue.get()
        html = retry.get_html(''.join(work_item[1:3]))
        if html is not None:
            soup = BeautifulSoup(html, features='html.parser')
            html_file.write(soup.prettify())
            logging.info(work_item[0])
            crawler_autotrader.crawl(soup, work_queue, work_item[1], json)

        work_queue.task_done()
    html_file.close()


def log(soup, enabled):
    if enabled is True:
        html_filename = '../log/log_' + datetime.now().strftime("%y-%m-%d_%H.%M") + '.html'
        with open(html_filename, 'w+', encoding='utf-8') as log_html:
            log_html.write(soup.prettify())
            log_html.close()
        copyfile(html_filename, '../log/logging.html')


def remove_last_comma(car_details_file):
    lines = open(car_details_file, 'r+').readlines()
    lines[-1] = lines[-1].replace(',', '')
    car_details_json = open(car_details_file, 'w+', encoding='utf-8')
    car_details_json.writelines(lines)
    car_details_json.close()


def start_crawler():
    logging.info("start_crawler")
    process_root('resources/sites.ini')
    car_details_file = 'data/car_details_' + datetime.now().strftime("%y-%m-%d_%H.%M") + '.json'

    car_details_json = open(car_details_file, 'w+', encoding='utf-8')
    car_details_json.write('[\n')
    process_work_queue(car_details_json)
    car_details_json.write(']')
    car_details_json.close()

    remove_last_comma(car_details_file)
    copyfile(car_details_file, 'data/car_details.json')


if __name__ == "__main__":
    start_crawler()
