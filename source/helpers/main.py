import unittest

from source.helpers.coupon_watch import CouponWatch
from source.helpers.tweet_feed import TwitterAPI


class TestTwitterBot(unittest.TestCase):

    def test_extract(self):
        self.twitter_api = TwitterAPI()
        self.twitter_api.extract_tweets()
        self.assertEqual(True, True)

    def test_stream(self):
        self.twitter_api = TwitterAPI()
        self.twitter_api.create_stream()
        while True:
            self.assertEqual(True, True)

    def test_extract_favs(self):
        self.twitter_api = TwitterAPI()
        favorites = self.twitter_api.extract_favorites()
        for favorite in favorites:
            print(favorite.created_at)
            self.assertGreater(favorite.id, 0)
        self.assertGreater(len(favorites), 0)

    def test_watch(self):
        self.watcher = CouponWatch()
        self.watcher.monitor()

    def test_get_coupon(self):
        self.watcher = CouponWatch()
        self.watcher.get_coupon_list()


if __name__ == '__main__':
    unittest.main()
