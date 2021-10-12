import tweepy
import os
from dotenv import load_dotenv

load_dotenv()
CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')


class TwitterAPI:
    def __init__(self):
        self.auth = {}
        self.api = {}
        self.user = "realDonaldTrump"

    def authenticate(self):
        # Authenticate to Twitter
        self.auth = tweepy.OAuthHandler("CONSUMER_KEY", CONSUMER_KEY)
        self.auth.set_access_token("ACCESS_TOKEN", ACCESS_TOKEN)
        return self.auth

    def create_api(self):
        # Create API object
        api = tweepy.API(self.authenticate())
        return api

    def extract_tweets(self):
        # Select user id
        user = self.user

        try:
            # Extract latest tweets
            tweets = self.create_api().user_timeline(screen_name=user,
                                                     # 200 is the maximum allowed count
                                                     count=200,
                                                     include_rts=False,
                                                     # Necessary to keep full_text
                                                     # otherwise only the first 140 words are extracted
                                                     tweet_mode='extended'
                                                     )
            # Show the extracted 3 latest tweets
            for info in tweets[:3]:
                print("ID: {}".format(info.id))
                print(info.created_at)
                print(info.full_text)
                print("\n")

        except:
            print('Invalid token.' + ACCESS_TOKEN)
