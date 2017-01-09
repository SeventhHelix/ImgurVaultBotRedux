__author__ = 'Jeff'

import string
import time
import requests
import random
import logging

import twitter
import imgurpython


TIME_BETWEEN_POST = 60 * 60 # seconds
IMGUR_URL = "http://i.imgur.com/%s.jpg"

api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')

logging.basicConfig(level=logging.INFO)


def generate_random_imgur_hash():
    return ''.join(random.sample(string.ascii_letters + string.digits, 6))


def get_random_imgur_link():
        imgur_link = None
        while not imgur_link:
            try:
                random_hash = generate_random_imgur_hash()
                attempt_link = IMGUR_URL % random_hash

                imgur_resp = requests.get(attempt_link)

                # Fail out of the attempt and retry if we get a 404
                if imgur_resp.url == u'http://i.imgur.com/removed.png' or imgur_resp.status_code == 404:
                    logging.info("Not a valid imgur hash: %s", attempt_link)
                    time.sleep(1)
                    continue

                imgur_link = attempt_link

            except Exception, e:
                logging.exception("Failed to get imgur image")
                time.sleep(1)

        return imgur_link


def main_loop():
    while True:
        imgur_link = get_random_imgur_link()
        logging.info("Posting imgur image: " + imgur_link)
        api.PostUpdate(imgur_link)

        time.sleep(TIME_BETWEEN_POST)


if __name__ == '__main__':
    main_loop()
