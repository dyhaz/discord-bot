import tweepy
import os
from dotenv import load_dotenv
import json

load_dotenv()
CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_FOLLOW_IDS = json.loads(os.getenv('TWITTER_FOLLOW_IDS'))


class TwitterAPI:
    def __init__(self):
        self.auth = {}
        self.api = {}
        self.stream = {}
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

    def extract_favorites(self):
        tweet_list = []
        for user_id in TWITTER_FOLLOW_IDS:
            tweet_list.append(self.create_api().get_favorites(user_id=user_id, count=10))
        for tweet in tweet_list:
            print(tweet)
        return tweet_list

    async def create_stream(self, discord_bot=None, follow_id=None):
        print('create stream...')
        self.stream = TweetStreamer(
            CONSUMER_KEY, CONSUMER_SECRET,
            ACCESS_TOKEN, ACCESS_TOKEN_SECRET
        )

        # Define who to follow
        if follow_id is None:
            follow_id = TWITTER_FOLLOW_IDS

        # Select bot to post messages
        self.stream.bot = discord_bot

        # Stream specific twitter ids
        self.stream.filter(follow=follow_id, threaded=True)

        # Stream hashtag
        # self.stream.filter(track=['#WELOVEYOUTWICE'], threaded=True)


class TweetStreamer(tweepy.Stream):

    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret):
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)
        self.bot = None

    def on_connection_error(self):
        print('stream error')
        if self.bot:
            self.bot.dispatch("stream_error")
        self.disconnect()

    def on_request_error(self, status_code):
        if self.bot:
            self.bot.dispatch("stream_error", status_code)

    def on_status(self, status):
        print(status.id)

    def on_data(self, raw_data):
        if self.bot:
            self.bot.dispatch("post_tweet", raw_data)

    def on_connect(self):
        print('stream connected')
