import tweepy
import os
from dotenv import load_dotenv

load_dotenv()
CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')


def authenticate():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler("CONSUMER_KEY", CONSUMER_KEY)
    auth.set_access_token("ACCESS_TOKEN", ACCESS_TOKEN)
    return auth


def create_api():
    # Create API object
    api = tweepy.API(authenticate())
    return api


def extract_tweets():
    # Select user id
    user = "realDonaldTrump"

    # Extract latest tweets
    tweets = create_api().user_timeline(screen_name=user,
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
