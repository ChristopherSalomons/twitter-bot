# Imports
import os
import tweepy
from dotenv import load_dotenv
from liz_framegrab import lizGetScreencap


# Load environment variables
load_dotenv()
bearer_token = os.getenv('LIZ_BEARER_TOKEN')
consumer_key = os.getenv('LIZ_API_KEY')
consumer_secret = os.getenv('LIZ_API_KEY_SECRET')
access_token = os.getenv('LIZ_ACCESS_TOKEN')
access_token_secret = os.getenv('LIZ_ACCESS_TOKEN_SECRET')


# Create Twitter API v1 object
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)


# Create Twitter API v2 object
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)
api = tweepy.API(auth)


# Create tweet
caption = lizGetScreencap()
dir_list = os.listdir("./liz_frames/jpg")
if not dir_list:
    print("Error: Missing screencap file")
else:
    filename = "./liz_frames/jpg/" + dir_list[0]
    api.update_status_with_media("", filename)