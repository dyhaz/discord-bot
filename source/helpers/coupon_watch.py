# Importing libraries
import time
import hashlib
import os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from sqlalchemy import insert, select, create_engine
import pymysql
import re

from source.helpers.web_parser import WebParser
from source.models.coupon import Coupon


def insert_data(url, desc, voucher_id):
    pymysql.install_as_MySQLdb()
    engine = create_engine(os.getenv('CONNECTION_URI'))

    with engine.connect() as connection:
        result = connection.execute(select(Coupon).where(Coupon.voucher_id == voucher_id and Coupon.url == url))
        if result.rowcount == 0:
            stmt = (
                insert(Coupon).values(name=desc.strip()[0:20], description=desc, url=url,
                                      voucher_id=int(voucher_id), is_deleted=False)
            )
            return connection.execute(stmt)
    return False


class CouponWatch:
    def __init__(self, discord_bot=None, base_url=None):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.base_url = 'https://www.cuponation.co.id/grabfood'
        self.discord_bot = None

        if base_url:
            self.base_url = base_url

        if discord_bot:
            self.discord_bot = discord_bot

        # setting the URL you want to monitor
        self.url = Request(self.base_url,
                           headers=self.headers)

    def watch_coupon(self):
        while True:
            if self.monitor():
                # get coupon operation
                self.get_coupon_list()

                # wait for 30 seconds
                time.sleep(30)
                self.watch_coupon()

    def watch_product(self):
        while True:
            if self.monitor():
                # get product
                self.get_product_info()

                # wait for 30 seconds
                time.sleep(30)
                self.watch_product()

    def monitor(self):
        print("running")
        time.sleep(10)
        while True:
            try:
                # to perform a GET request and load the
                # content of the website and store it in a var
                response = urlopen(self.url).read()

                # to create the initial hash
                current_hash = hashlib.sha224(response).hexdigest()

                # wait for 30 seconds
                time.sleep(30)

                # perform the get request
                response = urlopen(self.url).read()

                # create a new hash
                new_hash = hashlib.sha224(response).hexdigest()

                # check if new hash is same as the previous hash
                if new_hash == current_hash:
                    continue

                # if something changed in the hashes
                else:
                    # notify
                    print("something changed")
                    return True

            # To handle exceptions
            except Exception as e:
                print("error")
                return False

    def get_product_info(self):
        try:
            web_parse = WebParser(url=self.url)
            web_parse.get_price()
        # handle exceptions
        except Exception as e:
            print(f'Error during processing the request: '
                  f'{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}')

    def get_coupon_list(self):
        try:
            response = urlopen(self.url).read()
            soup = BeautifulSoup(response, features="html.parser")
            tags = [*soup.find_all(text="Kode"), *soup.find_all(text="Penawaran")]
            print(tags)
            for tag in tags:
                full_tag = tag.parent.parent.parent.parent.parent
                desc = full_tag.find('h3').get_text()
                if 'data-voucher-id' in full_tag.attrs:
                    voucher_id = full_tag.attrs['data-voucher-id']
                    url = self.get_full_url(voucher_id)

                    # Insert data to db if not exists
                    res = insert_data(url, desc, voucher_id)
                    if res and self.discord_bot:
                        # Send new inserted data
                        self.discord_bot.dispatch("post_coupon", desc, url)

        # handle exceptions
        except Exception as e:
            print(f'Error during processing the request: '
                           f'{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}')

    def get_full_url(self, voucher_id):
        # return the full url of current voucher_id
        return self.base_url + '#voucher-' + str(voucher_id)
