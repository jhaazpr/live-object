# Import Tweepy API components
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Utilities
import json
import re
import time
import pandas as pd
import matplotlib.pyplot as plt

# Access Variables. Required: secret.py
# !!! Do not push secret.py to a public repository !!!
import secret

import pylab

class StdOutListener(StreamListener):

    def __init__(self, output_file):
        self.output_file = output_file

    def on_data(self, data):
        self.output_file.write(data)
        # print data
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
        self.tweets = pd.DataFrame()
        self.tweets_file = open(tweets_file_name, 'r')
        for line in self.tweets_file:
            try:
                tweet = json.loads(line)
                self.tweets_data.append(tweet)
            except:
                continue

    def _word_in_text(self, word, text):
        word = word.lower()
        text = text.lower()
        match = re.search(word, text)
        if match:
            return True
        return False

    def do_lang(self):
        self.tweets['lang'] = map(lambda tweet: tweet['lang'], self.tweets_data)
        self.tweets_by_lang = self.tweets['lang'].value_counts()
        # Draw plot
        fig, ax = plt.subplots()
        ax.tick_params(axis='x', labelsize=15)
        ax.tick_params(axis='y', labelsize=10)
        ax.set_xlabel('Languages', fontsize=15)
        ax.set_ylabel('Number of tweets' , fontsize=15)
        ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
        self.tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
        pylab.show()

    def do_candidates(self):
        candidates = ['hilary', 'bernie', 'trump', 'cruz']
        self.tweets['text'] = map(lambda tweet: tweet['text'], self.tweets_data)

        self.tweets['hillary'] = self.tweets['text'].apply(lambda tweet: self._word_in_text('Hillary', tweet))
        self.tweets['bernie'] = self.tweets['text'].apply(lambda tweet: self._word_in_text('Bernie', tweet))
        self.tweets['trump'] = self.tweets['text'].apply(lambda tweet: self._word_in_text('Trump', tweet))
        self.tweets['cruz'] = self.tweets['text'].apply(lambda tweet: self._word_in_text('Cruz', tweet))

        tweet_counts_by_candidate = [
            self.tweets['hillary'].value_counts()[True],
            self.tweets['bernie'].value_counts()[True],
            self.tweets['trump'].value_counts()[True],
            self.tweets['cruz'].value_counts()[True]
        ]

        print tweet_counts_by_candidate

        # Draw plot
        x_pos = list(range(len(candidates)))
        width = 0.8
        fig, ax = plt.subplots()
        plt.bar(x_pos, tweet_counts_by_candidate, width, alpha=1, color='g')

        # Setting axis labels and ticks
        ax.set_ylabel('Number of tweets', fontsize=15)
        ax.set_title('Tweets by Candidate', fontsize=10, fontweight='bold')
        ax.set_xticks([p + 0.4 * width for p in x_pos])
        ax.set_xticklabels(candidates)
        plt.grid()
        pylab.show()


# MAIN FUNCTION
if __name__ == '__main__':

    auth_stream = AuthStream(secret.consumer_key,
                             secret.consumer_secret,
                             secret.access_token_key,
                             secret.access_token_secret)
    auth_stream.filter(['election', 'debate', 'usa', 'gop', 'democrat'], '../data/twitter_data.txt')
    tweet_parser = TweetsParser('../data/twitter_data.txt')
    tweet_parser.do_candidates()
