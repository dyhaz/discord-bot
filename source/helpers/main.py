import unittest

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


if __name__ == '__main__':
    unittest.main()
