# Import Tweepy API components
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import argparse
import time

# Access Variables. Required: secret.py
# !!! Do not push secret.py to a public repository !!!
import secret

class StdOutListener(StreamListener):

    def __init__(self, output_file):
        self.output_file = output_file

    def on_data(self, data):
        self.output_file.write(data)
        # print data
        return True

    def on_error(self, status):
        print status

class TweetStream():

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
    tweet_stream.filter(args.subjects, '../data/twitter_data.txt')
