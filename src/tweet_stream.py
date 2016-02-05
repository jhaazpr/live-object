# Import Tweepy API components
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# MongoDB
from pymongo import MongoClient

import argparse
import time
import json

# Access Variables. Required: secret.py
# !!! Do not push secret.py to a public repository !!!
import secret

class Listener(StreamListener):

    def __init__(self, db):
        self.db = db

    def on_data(self, data):
        # self.output_file.write(data)
        tweet = json.loads(data)
        self.db.insert(tweet)
        # print data
        return True

    def on_error(self, status):
        print status

class TweetStream():

    def __init__(self, consumer_key, consumer_secret, access_token_key, \
                 access_token_secret):
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token_key, access_token_secret)
        self.db = DB = MongoClient().test.tweets

    def filter(self, search_params):
        self.listener = Listener(self.db)
        self.stream = Stream(self.auth, self.listener)
        start_time = time.time()
        print 'Running stream with parameters {}.\n \
                Saving to MongoDB collection: db.test.tweets' \
                .format(search_params)
        try:
            self.stream.filter(track=search_params)
        except KeyboardInterrupt:
            print '\n\nRan stream for {} seconds'.format(time.time() - start_time)

# MAIN FUNCTION
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Search for tweets with given subjects')
    parser.add_argument('subjects', metavar='C', type=str, nargs='+',
                        help='a subject on twitter')
    args = parser.parse_args()
    print 'Searching for tweets with these subjects: {}...'.format(args.subjects)

    tweet_stream = TweetStream(secret.consumer_key,
                             secret.consumer_secret,
                             secret.access_token_key,
                             secret.access_token_secret)
    tweet_stream.filter(args.subjects)
