# Importing libraries
import time
import hashlib
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


class CouponWatch():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.base_url = 'https://www.cuponation.co.id/grabfood'

        # setting the URL you want to monitor
        self.url = Request(self.base_url,
                      headers=self.headers)

    def monitor(self):
        # to perform a GET request and load the
        # content of the website and store it in a var
        response = urlopen(self.url).read()

        # to create the initial hash
        currentHash = hashlib.sha224(response).hexdigest()
        print("running")
        time.sleep(10)
        while True:
            try:
                # perform the get request and store it in a var
                response = urlopen(self.url).read()

                # create a hash
                currentHash = hashlib.sha224(response).hexdigest()

                # wait for 30 seconds
                time.sleep(30)

                # perform the get request
                response = urlopen(self.url).read()

                # create a new hash
                newHash = hashlib.sha224(response).hexdigest()

                # check if new hash is same as the previous hash
                if newHash == currentHash:
                    continue

                # if something changed in the hashes
                else:
                    # notify
                    print("something changed")

                    # again read the website
                    response = urlopen(self.url).read()

                    # create a hash
                    currentHash = hashlib.sha224(response).hexdigest()

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

                # TODO: insert data to db if not exists
                # TODO: send message if new data

        # handle exceptions
        except Exception as e:
            print("Error fetching data")

    def get_full_url(self, voucher_id):
        return self.base_url + '#voucher-' + str(voucher_id)
