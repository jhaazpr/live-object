# Live Object 
Quasi-library for animating Internet of Things objects based on web data

### Getting Started
1. Install dependencies:

    `$ pip install tweepy`

    `$ pip install pandas`

    You may need to do additional installs if the script complains.

2. Obtain the secret.py file from another user. This file is
   not kept on the public repository.

3. Navigate to src/ . Run `python twitter_stream.py`. The script
   will the begin scraping twitter for election tweets and appending
   the data to `data/twitter_data.txt`. Once you've let the program
   scrape for long enough, hit `Ctrl-C`, and then the script will
   plot the results and return the percentage results of each
   category (here, presidential candidates).

4. For now, comment out the calls to `plot_candidates()` and/or
   `filter()` if you don't need plotting and/or more Twitter
   scraping. This will be cleaned up soon.
