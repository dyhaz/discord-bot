import unittest

from source.helpers.tweet_feed import TwitterAPI


class TestTwitterBot(unittest.TestCase):

    def test_extract(self):
        self.twitter_api = TwitterAPI()
        self.twitter_api.extract_tweets()
        self.assertEqual(True, True)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
