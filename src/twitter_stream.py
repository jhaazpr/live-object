# Import Tweepy API components
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Utilities
import json
import time
import pandas as pd
import matplotlib.pyplot as plt

# Access Variables. Required: secret.py
# !!! Do not push secret.py to a public repository !!!
import secret

class StdOutListener(StreamListener):

    def __init__(self, output_file):
        self.output_file = output_file

    def on_data(self, data):
        self.output_file.write(data)
        print data
        return True

    def on_error(self, status):
        print status

class AuthStream():

    def __init__(self, consumer_key, consumer_secret, access_token_key, \
                 access_token_secret):
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token_key, access_token_secret)

    def filter(self, search_params, output_file_name):
        f = open(output_file_name, 'a')
        self.listener = StdOutListener(f)
        self.stream = Stream(self.auth, self.listener)
        start_time = time.time()
        print 'Running stream with parameters {}.\n Saving to file: {} ...' \
                .format(search_params, output_file_name)
        try:
            self.stream.filter(track=search_params)
        except KeyboardInterrupt:
            f.flush()
            f.close()
            print '\n\nRan stream for {} seconds'.format(time.time() - start_time)

class TweetsParser():

    def __init__(self, tweets_file_name):
        self.tweets_data = []
        self.tweets_file = open(tweets_file_name, 'r')
        for line in self.tweets_file:
            tweet = json.loads(line)
            self.tweets_data.append(tweet)
        except:
            continue

    def _word_in_text(self, word, text):
        word = word.lower()
        text = text.lower()
        match = re.search(word, text)
        return match

# MAIN FUNCTION
if __name__ == '__main__':

    auth_stream = AuthStream(secret.consumer_key,
                             secret.consumer_secret,
                             secret.access_token_key,
                             secret.access_token_secret)
    auth_stream.filter(['python, javascript', 'ruby'], '../data/twitter_data.txt')

