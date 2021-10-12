import tweepy
import os
from dotenv import load_dotenv

load_dotenv()
CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

class TwitterAPI:
    def __init__(self):
        self.auth = {}
        self.api = {}
        self.user = "alhadie_"

    def authenticate(self):
        # Authenticate to Twitter
        if not self.auth:
            self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        return self.auth

    def create_api(self):
        # Create API object
        if not self.api:
            self.api = tweepy.API(self.authenticate())

        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except:
            print("Error during authentication")

        return self.api

    def extract_tweets(self):
        # Select user id
        user = self.user

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
