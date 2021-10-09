
import logging
import time
from functools import wraps
from urllib.request import Request, urlopen

def retry(exceptions=Exception, retries=5, backoff=2):
    def decorate(func):
        @wraps(func)
        def call(*args, **kwargs):
            retry_count = 0
            while retry_count < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    retry_count += 1
                    logging.fatal(f'failed count:{retry_count} to get {err}')
                    time.sleep(backoff)
        return call
    return decorate


@retry()
def get_html(url):
    logging.info('processing link: {}'.format(url))
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    return urlopen(req).read()
