# Utilities
import json
import re
import time
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import pylab

class TweetsParser():

    def __init__(self, tweets_file_name, candidates):
        self.tweets_data = []
        self.tweets = pd.DataFrame()
        self.tweets_file = open(tweets_file_name, 'r')
        for line in self.tweets_file:
            try:
                tweet = json.loads(line)
                self.tweets_data.append(tweet)
            except:
                continue

        # Result data
        self.candidates = candidates
        self.candidate_counts = []

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

    def calc_candidate_counts(self):
        self.tweets['text'] = map(lambda tweet: tweet['text'], self.tweets_data)

        # TODO: replace with better candidate recognition than just raw text e.g. #feelthebern
        # self.tweets['hillary'] = self.tweets['text'].apply(lambda tweet: self._word_in_text('Hillary', tweet))
        # self.tweets['bernie'] = self.tweets['text'].apply(lambda tweet: self._word_in_text('Bernie', tweet))
        # self.tweets['trump'] = self.tweets['text'].apply(lambda tweet: self._word_in_text('Trump', tweet))
        # self.tweets['cruz'] = self.tweets['text'].apply(lambda tweet: self._word_in_text('Cruz', tweet))

        for candidate in self.candidates:
            self.tweets[candidate] = self.tweets['text'].apply(lambda tweet: self._word_in_text(candidate, tweet))

        # self.candidate_counts = [
        #     self.tweets['hillary'].value_counts()[True],
        #     self.tweets['bernie'].value_counts()[True],
        #     self.tweets['trump'].value_counts()[True],
        #     self.tweets['cruz'].value_counts()[True]
        # ]

        self.candidate_counts = [self.tweets[candidate].value_counts()[True] for candidate in self.candidates]

        return self.candidate_counts

    def plot_candidates(self):
        # Draw plot
        x_pos = list(range(len(self.candidates)))
        width = 0.8
        fig, ax = plt.subplots()
        plt.bar(x_pos, self.candidate_counts, width, alpha=1, color='g')

        # Setting axis labels and ticks
        ax.set_ylabel('Number of tweets', fontsize=15)
        ax.set_title('Tweets by Candidate', fontsize=10, fontweight='bold')
        ax.set_xticks([p + 0.4 * width for p in x_pos])
        ax.set_xticklabels(self.candidates)
        plt.grid()
        pylab.show()

    def _word_in_text(self, word, text):
        word = word.lower()
        text = text.lower()
        match = re.search(word, text)
        if match:
            return True
        return False

    def calc_normalize_counts(self):
        total_tweets = float(reduce(lambda x, y: x + y, self.candidate_counts))
        return [tweet_count / total_tweets for tweet_count in self.candidate_counts]


# MAIN FUNCTION
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find tweet counts of candidates')
    parser.add_argument('candidates', metavar='C', type=str, nargs='+',
                        help='a candidate\'s name')
    args = parser.parse_args()

    tweets_parser = TweetsParser('../data/twitter_data.txt', args.candidates)

    while True:
        try:
            candidate_counts = tweets_parser.calc_candidate_counts()
            # TODO: add command line args for plotting. For now, comment out if you don't want plots
            print tweets_parser.calc_normalize_counts()
            # tweets_parser.plot_candidates()
            time.sleep(5)
        except KeyboardInterrupt:
            exit()
