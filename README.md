# Live Object
Quasi-library for animating Internet of Things objects based on web data

### Getting Started
1. Install dependencies:

    `$ pip install tweepy`

    `$ pip install pandas`

    `$ pip install pymongo`

    More information about hooking up the Python wrapper for MongoDB
    can be found [here](https://docs.mongodb.org/getting-started/python/client/).
    You may need to do additional installs if the script complains.

2. Obtain the secret.py file from another user. This file is
   not kept on the public repository.

3. Run `$ mongod` in another tab.

4. Navigate to src/ . Run `python twitter_stream.py [arg_1 ... arg_n]`.
   The script will begin scraping twitter for tweets with
   `arg_i` and save matching tweets to the running MongoDB
   instance. This is our data stream.

5. Go to the following piece of code in `affect_model.py`

`        self.fans = [
            SmartFan(candidates[0], {{ PORT }}),
            SmartFan(candidates[1], {{ PORT }})
         ]
`
   And change the port numbers (second argument) to match those
   on your computer. Thus, candidate i is represented by port i.

6. Run `python affect_model.py neutral acceleration bernie hillary`, or
   replace the candidates' names to any candidate. This should be done
   while the data stream is running. The program will continuously print
   the tweet acceleration and pipe fan strengths to the fans. Be patient
   at first; the accelerations will be 0.0 for the first couple of
   seconds.
