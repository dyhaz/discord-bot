# Importing libraries
import time
import hashlib
import os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from sqlalchemy import insert, select, create_engine
import pymysql

from source.models.coupon import Coupon


def insert_data(url, desc, voucher_id):
    pymysql.install_as_MySQLdb()
    engine = create_engine(os.getenv('CONNECTION_URI'))

    with engine.connect() as connection:
        result = connection.execute(select(Coupon).where(Coupon.voucher_id == voucher_id))
        if result.rowcount == 0:
            stmt = (
                insert(Coupon).values(name=desc.strip()[0:20], description=desc, url=url,
                                      voucher_id=int(voucher_id), is_deleted=False)
            )
            return connection.execute(stmt)
    return False


class CouponWatch:
    def __init__(self, discord_bot=None):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.base_url = 'https://www.cuponation.co.id/grabfood'
        self.discord_bot = None
        if discord_bot:
            self.discord_bot = discord_bot

        # setting the URL you want to monitor
        self.url = Request(self.base_url,
                           headers=self.headers)

    def monitor(self):
        # to perform a GET request and load the
        # content of the website and store it in a var
        response = urlopen(self.url).read()

        # to create the initial hash
        current_hash = hashlib.sha224(response).hexdigest()
        print("running")
        time.sleep(10)
        while True:
            try:
                # perform the get request and store it in a var
                response = urlopen(self.url).read()

                # create a hash
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

                    # get coupon operation
                    self.get_coupon_list()

                    # wait for 30 seconds
                    time.sleep(30)
                    continue

            # To handle exceptions
            except Exception as e:
                print("error")

    def get_coupon_list(self):
        try:
            response = urlopen(self.url).read()
            soup = BeautifulSoup(response, features="html.parser")
            tags = soup.find_all(text="Kode")
            for tag in tags:
                full_tag = tag.parent.parent.parent.parent.parent
                desc = full_tag.find('h3').get_text()
                voucher_id = full_tag.attrs['data-voucher-id']
                url = self.get_full_url(voucher_id)

                # Insert data to db if not exists
                if insert_data(url, desc, voucher_id) and self.discord_bot:
                    # Send new inserted data
                    self.discord_bot.dispatch("post_coupon", desc, url)

        # handle exceptions
        except Exception as e:
            print(f'Error during processing the request: '
                           f'{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}')

    def get_full_url(self, voucher_id):
        # return the full url of current voucher_id
        return self.base_url + '#voucher-' + str(voucher_id)
